# deepstream_analysis.py
import sys
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, GLib
import pyds

# Initialize GStreamer
Gst.init(None)

def osd_sink_pad_buffer_probe(pad, info, u_data):
    frame_number = 0
    obj_counter = {}
    
    gst_buffer = info.get_buffer()
    if not gst_buffer:
        print("Unable to get GstBuffer ")
        return

    batch_meta = pyds.gst_buffer_get_nvds_batch_meta(hash(gst_buffer))
    l_frame = batch_meta.frame_meta_list

    while l_frame is not None:
        try:
            frame_meta = pyds.NvDsFrameMeta.cast(l_frame.data)
        except StopIteration:
            break

        frame_number = frame_meta.frame_num
        l_obj = frame_meta.obj_meta_list

        while l_obj is not None:
            try:
                obj_meta = pyds.NvDsObjectMeta.cast(l_obj.data)
            except StopIteration:
                break

            obj_class = obj_meta.class_id
            if obj_class == 0:
                obj_counter['gun'] += 1
            elif obj_class == 2:
                obj_counter['knive'] += 1

            try:
                l_obj = l_obj.next
            except StopIteration:
                break

        try:
            l_frame = l_frame.next
        except StopIteration:
            break

    return Gst.PadProbeReturn.OK

def analyze_video(video_path):
    # Standard GStreamer initialization
    print("Creating Pipeline \n ")
    pipeline = Gst.parse_launch(
        "filesrc location={} ! decodebin ! nvinfer config-file-path=config_infer_primary.txt ! nvvideoconvert ! nvdsosd ! nvvideoconvert ! autovideosink".format(video_path)
    )

    # Create an event loop and feed GStreamer bus mesages to it
    loop = GLib.MainLoop()
    bus = pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect("message", bus_call, loop)

    # Add a probe to get informed of the meta data generated, we add probe to
    # the sink pad of the osd element, since by that time, the buffer would
    # have had got all the metadata.
    osdsinkpad = pipeline.get_by_name("nvdsosd").get_static_pad("sink")
    if not osdsinkpad:
        sys.stderr.write(" Unable to get sink pad of nvdsosd \n")
    else:
        osdsinkpad.add_probe(Gst.PadProbeType.BUFFER, osd_sink_pad_buffer_probe, 0)

    # Start play back and listen to events
    print("Starting pipeline \n")
    pipeline.set_state(Gst.State.PLAYING)
    try:
        loop.run()
    except:
        pass

    # Cleanup
    print("Exiting app\n")
    pipeline.set_state(Gst.State.NULL)

    # Return the results (this should be adjusted based on actual requirements)
    return {"message": "Video analysis completed", "details": "Object counts and other details"}

def bus_call(bus, message, loop):
    t = message.type
    if t == Gst.MessageType.EOS:
        print("End-of-stream\n")
        loop.quit()
    elif t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print("Error: %s: %s\n" % (err, debug))
        loop.quit()
    return True
