0: read code. clean folder structure
1: rotation
2: inelastic ollision
3: seperate into levels.
atomic (proton, electron)
mechanical (objects. magic ground magic forces magic g for gravity)
planetary (planets. has gravitation force.)

maybe later add quantum and molecular but not now
4: optimize BIN format!  
no need to repeately store object vertices structure each frame. 


Change the format to:                                                     
                                                                            
  Header:                                                                   
    magic, fps, total_frames, etc                                           
                                                                            
  Mesh table (once):                                                        
    object_count                                                            
    for each object:                                                        
      id, vertices, indices, color                                          
                                                                            
  Frames:                                                                   
    for each frame:                                                         
      time                                                                  
      for each object:                                                      
        object_index (uint16 - reference to mesh table)                     
        position (3 floats)                                                 
        rotation (9 floats)      





4: camera selection object with a,d cycling

5: scene edits. this should have both an api and a UI. the api could be used as a sort of evolutionary design to iterate on robotic designs! like NAS for algorithms this is like design search for robots!  

6: robotic simulation with neural control api

7: gradually implement electricity
( at this point it could be quite cool we can actually simulate linear motors or whatever)


