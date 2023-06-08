import bpy
from bpy.props import IntProperty

class SetSamples(bpy.types.Operator):
    '''Blender Modal Operator'''
    bl_idname = 'render.set_cycles_samples'
    bl_label = 'Set Cycles Samples'
    samples : IntProperty(
        name="samples",
        min=0,
        default=20
    )
    timer = None
    
    def execute(self, context):
        # in execute method we just create a timer and add a modal handler
        # which handles events in real-time. We set the timer to the class
        # variable to be able to remove it later on.
        self.timer = bpy.context.window_manager.event_timer_add(.1, window=context.window)
        bpy.context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'} # this starts the modal() method
    
    def modal(self, context, event):
        # modal handles events in real-time
        if event.type == 'ESC':
            # in case something goes wrong and we need to abort it manually
            bpy.context.window_manager.event_timer_remove(self.timer) # remove timer
            return {'CANCELLED'} 
        elif event.type == 'TIMER':
            print('Tick!') # just a test to count how many times timer ticks
            # on every Timer tick the Operator checks: 
            if context.scene.cycles.samples == self.samples:
                # if everything worked correctly and Cycles samples have changed:
                bpy.context.window_manager.event_timer_remove(self.timer) # remove timer
                bpy.ops.render.render('INVOKE_DEFAULT') # render 
                print('FINISHED') # just a test message after
                return {'FINISHED'}
            else:
                # if samples haven't changed:
                context.scene.cycles.samples = self.samples # command to change samples
                context.scene.update_tag() # not sure what it does but it was recommended
                                           # in the comments to the question
                print(f'Cycles samples after changing: {context.scene.cycles.samples}') # test message 
        return {'PASS_THROUGH'} # returns us to the start of the modal() method
        
    def invoke(self, context, event):
        # Operator starts to execute from here when called with ('INVOKE_DEFAULT'),
        # like if it was called by user, not by script      
        return self.execute(context) # this starts the execute() method
    
def register():
    # as we use the Blender Operator class, it needs to be registered:
    bpy.utils.register_class(SetSamples)

def unregister():
    bpy.utils.unregister_class(SetSamples)

if __name__ == "__main__":
    register()
    # after register you can use your Operator just like any other Operator in Blender
    # the last parameter is the samples you need
    bpy.ops.render.set_cycles_samples('INVOKE_DEFAULT', samples = 20) 