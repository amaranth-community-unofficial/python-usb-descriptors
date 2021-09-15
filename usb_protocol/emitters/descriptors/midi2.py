#
# This file is part of usb_protocol.
#
""" Convenience emitters for USB MIDI Class 2 descriptors. """

from .. import emitter_for_format
from ...types.descriptors.midi2 import *

StandardMidiStreamingInterfaceDescriptorEmitter            = emitter_for_format(StandardMidiStreamingInterfaceDescriptor)
ClassSpecificMidiStreamingInterfaceHeaderDescriptorEmitter = emitter_for_format(ClassSpecificMidiStreamingInterfaceHeaderDescriptor)
StandardMidiStreamingDataEndpointDescriptorEmitter         = emitter_for_format(StandardMidiStreamingDataEndpointDescriptor)