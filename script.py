import mdl
from display import *
from matrix import *
from draw import *

"""======== first_pass( commands ) ==========

  Checks the commands array for any animation commands
  (frames, basename, vary)

  Should set num_frames and basename if the frames
  or basename commands are present

  If vary is found, but frames is not, the entire
  program should exit.

  If frames is found, but basename is not, set name
  to some default value, and print out a message
  with the name being used.
  ==================== """

def first_pass( commands ):
    name = ''
    num_frames = 1
    vary = False
    for command in commands:
	if command['op'] == 'frames':
	    num_frames = command['args'][0]
	elif command['op'] == 'basename':
	    name = command['args'][0]
	elif command['op'] == 'vary':
	    vary = True	    
    if name == '':
	print 'No name found. Setting to default name \"anim\"'
    	name = 'anim'
    if vary and num_frames == 1:
	raise('ERROR: Vary found but only 1 frame. Exiting program.')
    return (name, num_frames)

"""======== second_pass( commands ) ==========

  In order to set the knobs for animation, we need to keep
  a seaprate value for each knob for each frame. We can do
  this by using an array of dictionaries. Each array index
  will correspond to a frame (eg. knobs[0] would be the first
  frame, knobs[2] would be the 3rd frame and so on).

  Each index should contain a dictionary of knob values, each
  key will be a knob name, and each value will be the knob's
  value for that frame.

  Go through the command array, and when you find vary, go
  from knobs[0] to knobs[frames-1] and add (or modify) the
  dictionary corresponding to the given knob with the
  appropirate value.
  ===================="""
def second_pass( commands, num_frames, symbols ):
    frames = [ {} for i in range(int(num_frames)) ]
    for command in commands:
        if command['op'] == 'vary':
            if len(command['args']) == 4:
                start_frame, end_frame = command['args'][0], command['args'][1]
                start_mag, end_mag = command['args'][2], command['args'][3]
                change_mag = (end_mag - start_mag) / (end_frame - start_frame)
                frame = start_frame
                mag = start_mag
                while frame <= end_frame:
                    frames[int(frame)][command['knob']] = mag
                    frame += 1
                    mag += change_mag
            else:
                for find_vary in commands:
                    if 'knob' in find_vary and command['knob'] == find_vary['knob'] and not find_vary['args']:
                        break
                source = symbols[find_vary['light']][1]
                start_frame, end_frame = command['args'][0], command['args'][1]
                
                change_x = command['args'][2] - source['location'][0]
                change_y = command['args'][3] - source['location'][1]
                change_z = command['args'][4] - source['location'][2]
                change_r = command['args'][5] - source['color'][0]
                change_g = command['args'][6] - source['color'][1]
                change_b = command['args'][7] - source['color'][2]
                
                frame = start_frame
                frame_change = end_frame - start_frame
                
                frames[int(frame)][command['knob']] = 0
                while frame <= end_frame:
                    new_frame_change = (frame - start_frame) / frame_change
                    frames[int(frame)][command['knob']] = [new_frame_change * change_x, new_frame_change * change_y,
                        new_frame_change * change_z, new_frame_change * change_r, new_frame_change * change_g,
                        new_frame_change * change_b]
                    frame += 1             
    return frames


def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]

    color = [0, 0, 0]
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    normal_hash_table = dict()

    (name, num_frames) = first_pass(commands)
    frames = second_pass(commands, num_frames, symbols)
    
    current_frame = 0
    while current_frame < num_frames:
        print 'Generating frame ' + str(current_frame)
        tmp = new_matrix()
        ident( tmp )
        stack = [ [x[:] for x in tmp] ]
        screen = new_screen()
    	zbuffer = new_zbuffer()
        tmp = []
        step_3d = 100
        consts = ''
        coords = []
        coords1 = []
        
        light = 'lol'
        
        for symbol in symbols:
            if current_frame >= 1 and symbols[symbol][0] == 'light' and symbols[symbol][1]['knob']:
                new = frames[current_frame][symbols[symbol][1]['knob']]

                symbols[symbol][1]['color'][0] += new[3] / current_frame
                symbols[symbol][1]['color'][1] += new[4] / current_frame
                symbols[symbol][1]['color'][2] += new[5] / current_frame
                symbols[symbol][1]['location'][0] += new[0] / current_frame
                symbols[symbol][1]['location'][1] += new[1] / current_frame
                symbols[symbol][1]['location'][2] += new[2] / current_frame


        for command in commands:	
            c = command['op']
            args = command['args']

            if c == 'box':
                if command['constants']:
                    reflect = command['constants']
                add_box(tmp,
                        args[0], args[1], args[2],
                        args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'sphere':
                if command['constants']:
                    reflect = command['constants']
                add_sphere(tmp,
                           args[0], args[1], args[2], args[3], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'torus':
                if command['constants']:
                    reflect = command['constants']
                add_torus(tmp,
                          args[0], args[1], args[2], args[3], args[4], step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
                tmp = []
                reflect = '.white'
            elif c == 'line':
                add_edge(tmp,
                         args[0], args[1], args[2], args[3], args[4], args[5])
                matrix_mult( stack[-1], tmp )
                draw_lines(tmp, screen, zbuffer, color)
                tmp = []
            elif c == 'move':
                knob = frames[current_frame][command['knob']] if command['knob'] else 1
                tmp = make_translate(args[0] * knob, args[1] * knob, args[2] * knob)	              
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'scale':
                knob = frames[current_frame][command['knob']] if command['knob'] else 1
                tmp = make_scale(args[0] * knob, args[1] * knob, args[2] * knob)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'rotate':
                knob = frames[current_frame][command['knob']] if command['knob'] else 1
                theta = args[1] * (math.pi/180)
                if args[0] == 'x':
                    tmp = make_rotX(theta * knob)
                elif args[0] == 'y':
                    tmp = make_rotY(theta * knob)
                else:
                    tmp = make_rotZ(theta * knob)
                matrix_mult( stack[-1], tmp )
                stack[-1] = [ x[:] for x in tmp]
                tmp = []
            elif c == 'push':
                stack.append([x[:] for x in stack[-1]] )
            elif c == 'pop':
                stack.pop()
            elif c == 'display':
                display(screen)
            elif c == 'save':
                save_extension(screen, args[0])
            
    	current_frame += 1
        if num_frames < 100:
            save_extension(screen, 'anim/' + name + "%02d"%current_frame)
        else:
            save_extension(screen, 'anim/' + name + "%03d"%current_frame)
    if num_frames > 1:
        make_animation( name)
