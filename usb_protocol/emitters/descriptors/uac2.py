#
# This file is part of usb_protocol.
#
""" Convenience emitters for USB Audio Class 2 descriptors. """

from contextlib import contextmanager

from .. import emitter_for_format
from ...types.descriptors.uac2 import *
from ...emitters.descriptor    import ComplexDescriptorEmitter

# Create our emitters.
InterfaceAssociationDescriptorEmitter          = emitter_for_format(InterfaceAssociationDescriptor)
StandardAudioControlInterfaceDescriptorEmitter = emitter_for_format(StandardAudioControlInterfaceDescriptor)

class ClassSpecificAudioControlInterfaceDescriptorEmitter(ComplexDescriptorEmitter):
    DESCRIPTOR_FORMAT = ClassSpecificAudioControlInterfaceDescriptor

    def _pre_emit(self):
        # Figure out the total length of our descriptor, including subordinates.
        subordinate_length = sum(len(sub) for sub in self._subordinates)
        self.wTotalLength = subordinate_length + self.DESCRIPTOR_FORMAT.sizeof()

ClockSourceDescriptorEmitter                                             = emitter_for_format(ClockSourceDescriptor)
ClockSelectorDescriptorElementEmitter                                    = emitter_for_format(ClockSelectorDescriptorElement)
ClockSelectorDescriptorFootEmitter                                       = emitter_for_format(ClockSelectorDescriptorFoot)
InputTerminalDescriptorEmitter                                           = emitter_for_format(InputTerminalDescriptor)
OutputTerminalDescriptorEmitter                                          = emitter_for_format(OutputTerminalDescriptor)
AudioStreamingInterfaceDescriptorEmitter                                 = emitter_for_format(AudioStreamingInterfaceDescriptor)
ClassSpecificAudioStreamingInterfaceDescriptorEmitter                    = emitter_for_format(ClassSpecificAudioStreamingInterfaceDescriptor)
TypeIFormatTypeDescriptorEmitter                                         = emitter_for_format(TypeIFormatTypeDescriptor)
ExtendedTypeIFormatTypeDescriptorEmitter                                 = emitter_for_format(ExtendedTypeIFormatTypeDescriptor)
TypeIIFormatTypeDescriptorEmitter                                        = emitter_for_format(TypeIIFormatTypeDescriptor)
ExtendedTypeIIFormatTypeDescriptorEmitter                                = emitter_for_format(ExtendedTypeIIFormatTypeDescriptor)
TypeIIIFormatTypeDescriptorEmitter                                       = emitter_for_format(TypeIIIFormatTypeDescriptor)
ExtendedTypeIIIFormatTypeDescriptorEmitter                               = emitter_for_format(ExtendedTypeIIIFormatTypeDescriptor)
ClassSpecificAudioStreamingIsochronousAudioDataEndpointDescriptorEmitter = emitter_for_format(ClassSpecificAudioStreamingIsochronousAudioDataEndpointDescriptor)
AudioControlInterruptEndpointDescriptorEmitter                           = emitter_for_format(AudioControlInterruptEndpointDescriptor)
AudioStreamingIsochronousEndpointDescriptorEmitter                       = emitter_for_format(AudioStreamingIsochronousEndpointDescriptor)
AudioStreamingIsochronousFeedbackEndpointDescriptorEmitter               = emitter_for_format(AudioStreamingIsochronousFeedbackEndpointDescriptor)

class ClockSelectorDescriptorEmitter(ComplexDescriptorEmitter):
    DESCRIPTOR_FORMAT = ClockSelectorDescriptorHead
    _controls_added = False

    def add_subordinate_descriptor(self, subordinate):
        subordinate = subordinate.emit()
        self._subordinates.append(subordinate)

    def add_source(self, cSourceId):
        sourceDescriptor = ClockSelectorDescriptorElementEmitter()
        sourceDescriptor.baCSourceID = cSourceId
        self.add_subordinate_descriptor(sourceDescriptor)

    def add_controls(self, clockFreqControl: ClockFrequencyControl, iClockSelector: int=0):
        clockSelectorFoot = ClockSelectorDescriptorFootEmitter()
        clockSelectorFoot.bmControls = clockFreqControl
        clockSelectorFoot.iClockSelector = iClockSelector
        self.add_subordinate_descriptor(clockSelectorFoot)
        self._controls_added = True

    def _pre_emit(self):
        if not self._controls_added:
            self.add_subordinate_descriptor(ClockSelectorDescriptorFootEmitter())
        # Figure out the total length of our descriptor, including subordinates.
        subordinate_length = sum(len(sub) for sub in self._subordinates)
        self.bLength = subordinate_length + self.DESCRIPTOR_FORMAT.sizeof()
