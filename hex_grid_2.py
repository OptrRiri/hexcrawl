print("\n\n\n\n-------------------------------------------------------------------------------------------")
# --- Imports ---
if True: 
    from importlib.resources import path
    import winsound
    import pygame
    from math import sqrt
    from random import randint
    import openpyxl
    import numpy
    import decimal
    from decimal import Decimal, InvalidOperation

# --- Classes --- (CamelCase)
class Hex:
    def __init__(self, 
                 coord_x, 
                 coord_y,) -> None:

        self.coord_x = coord_x
        self.coord_y = coord_y
        self.id = f"{coord_x},{coord_y}"
        self.adjacent_hexes = {"northwest":None, 
                               "northeast":None, 
                               "east":None,
                               "southeast":None, 
                               "southwest":None, 
                               "west":None}
        self.skew = ">" if int(self.coord_y) % 2 == 0 else "<"
        self.data = {"primary_terrain":"undetermined", 
                     "hex_rects/surfaces_dict":{}}
        self.center_calculated = False
        pass

    def blit_hex(self, zoom, center:tuple=None):
        #self.data["hex_rects/surfaces_dict"][zoom]["rects"]["surface_rect"].center = center
        self.data["hex_rects/surfaces_dict"][zoom]["surface"]["main"].blit(self.data["hex_rects/surfaces_dict"][zoom]["surface"]["label"], self.data["hex_rects/surfaces_dict"][zoom]["rects"]["label_rect"])
        screen.blit(self.data["hex_rects/surfaces_dict"][zoom]["surface"]["main"], self.data["hex_rects/surfaces_dict"][zoom]["rects"]["surface_rect"])

        pass

class HexGrid:
    def __init__(self, 
                 max_x:int=10, 
                 max_y:int=10, 
                 min_x:int=None, 
                 min_y:int=None) -> None:
        
        self.max_x = max_x
        self.max_y = max_y
        self.min_x = max_x * -1 if min_x == None else min_x
        self.min_y = max_y * -1 if min_y == None else min_y

        self.hex_dict = {}
        for x in range(self.min_x, self.max_x+1): # hex creation
            for y in range(self.min_y, self.max_y+1):
                self.hex_dict[f"{x},{y}"] = Hex(x,y)

        for hex in self.hex_dict.values(): # hex linking
            x_holder = hex.coord_x
            y_holder = hex.coord_y
            
            if hex.skew == ">":
                adj_dict = {"northwest":f"{x_holder},{y_holder+1}", 
                            "northeast":f"{x_holder+1},{y_holder+1}", 
                            "east":f"{x_holder+1},{y_holder}",
                            "southeast":f"{x_holder+1},{y_holder-1}", 
                            "southwest":f"{x_holder},{y_holder-1}", 
                            "west":f"{x_holder-1},{y_holder}",}
            
            elif hex.skew == "<":
                adj_dict = {"northwest":f"{x_holder-1},{y_holder+1}", 
                            "northeast":f"{x_holder},{y_holder+1}", 
                            "east":f"{x_holder+1},{y_holder}",
                            "southeast":f"{x_holder},{y_holder-1}", 
                            "southwest":f"{x_holder-1},{y_holder-1}", 
                            "west":f"{x_holder-1},{y_holder}",}

            for direction in hex.adjacent_hexes.keys():
                try:
                    hex.adjacent_hexes[direction] = self.hex_dict[adj_dict[direction]] 
                except KeyError: 
                    pass
        
        pass

    def calculate_centers(self, 
                          outer_rad_input=70, 
                          current_zoom=1.0, 
                          coord_of_00=None):

        for hex in self.hex_dict.values(): # resetting statuses
            hex.center_calculated = False
        
        hex_00 = hex_grid.hex_dict["0,0"]

        if coord_of_00 == None:
            hex_00.data["hex_rects/surfaces_dict"][current_zoom]["rects"]["surface_rect"].center = (SCREEN_WIDTH/2, EFFECTIVE_SCREEN_HEIGHT/2)
        else:
            hex_00.data["hex_rects/surfaces_dict"][current_zoom]["rects"]["surface_rect"].center = coord_of_00

        hex_00.center_calculated = True

        x_coord = hex_00.data["hex_rects/surfaces_dict"][current_zoom]["rects"]["surface_rect"].center[0]
        y_coord = hex_00.data["hex_rects/surfaces_dict"][current_zoom]["rects"]["surface_rect"].center[1]

        outer_rad = outer_rad_input * current_zoom
        alp = outer_rad/4
        bet = sqrt(3)*alp

        for direction in hex_00.adjacent_hexes.keys():
            try:
                if direction == "northwest":
                    new_coord_center = (x_coord-bet, y_coord-(3*alp))
                elif direction == "northeast":
                    new_coord_center = (x_coord+bet, y_coord-(3*alp))
                elif direction == "east":
                    new_coord_center = (x_coord+2*(bet), y_coord)
                elif direction == "southeast":
                    new_coord_center = (x_coord+bet, y_coord+(3*alp))
                elif direction == "southwest":
                    new_coord_center = (x_coord-bet, y_coord+(3*alp))
                elif direction == "west":
                    new_coord_center = (x_coord-2*(bet), y_coord)

                hex_00.adjacent_hexes[direction].data["hex_rects/surfaces_dict"][current_zoom]["rects"]["surface_rect"].center = new_coord_center
                hex_00.adjacent_hexes[direction].center_calculated = True
            
            except TypeError:
                pass

        keepGoing = True
        while keepGoing == True:
            completion_tracker = [hexblade.center_calculated for hexblade in self.hex_dict.values()]
            print(f"yurayurayura {completion_tracker.count(False)}/{len(completion_tracker)}")
            if False not in completion_tracker:
                keepGoing = False
            else:
                for hexbald in self.hex_dict.values():
                    if hexbald.center_calculated == True:
                        try:
                            x_coord = hexbald.data["hex_rects/surfaces_dict"][current_zoom]["rects"]["surface_rect"].center[0]
                            y_coord = hexbald.data["hex_rects/surfaces_dict"][current_zoom]["rects"]["surface_rect"].center[1]

                            for direction in hexbald.adjacent_hexes.keys():
                                try:
                                    if direction == "northwest":
                                        new_coord_center = (x_coord-bet, y_coord-(3*alp))
                                    elif direction == "northeast":
                                        new_coord_center = (x_coord+bet, y_coord-(3*alp))
                                    elif direction == "east":
                                        new_coord_center = (x_coord+2*(bet), y_coord)
                                    elif direction == "southeast":
                                        new_coord_center = (x_coord+bet, y_coord+(3*alp))
                                    elif direction == "southwest":
                                        new_coord_center = (x_coord-bet, y_coord+(3*alp))
                                    elif direction == "west":
                                        new_coord_center = (x_coord-2*(bet), y_coord)

                                    if hexbald.adjacent_hexes[direction].center_calculated == False:
                                        hexbald.adjacent_hexes[direction].data["hex_rects/surfaces_dict"][current_zoom]["rects"]["surface_rect"].center = new_coord_center
                                        hexbald.adjacent_hexes[direction].center_calculated = True
                                    else:pass
                                
                                except AttributeError:
                                    pass

                        except TypeError:
                            pass

        pass

    def get_coords_of_rc(self, rc:str="row", coord = 0):
        return_dict = {}
        if rc == "row":
            for hex in hex_grid.hex_dict.values():
                
                pass
        elif rc == "col":
            pass
        return return_dict

# --- Functions --- (lower_case)    
def generate_hex_points_from_center(center_coord:tuple, radius:float):
    return_dict = {}

    outer_rad = radius
    alp = outer_rad/4
    bet = sqrt(3)*alp

    x_coord = center_coord[0]
    y_coord = center_coord[1]

    return_dict["topleft"]=(x_coord-bet, y_coord-alp)
    return_dict["top"]=(x_coord, y_coord-(0.5*(outer_rad)))
    return_dict["topright"]=(x_coord+bet, y_coord-alp)
    return_dict["botright"]=(x_coord+bet, y_coord+alp)
    return_dict["bot"]=(x_coord, y_coord+(0.5*(outer_rad)))
    return_dict["botleft"]=(x_coord-bet, y_coord+alp)
    
    return return_dict

def doSomething():
    return None

def getFont(font_size, font_style="freesansbold.ttf"):
    global font_dict
    string_hold = f"{font_style}_{font_size}"
    if string_hold not in font_dict.keys():
        font_dict[string_hold] = pygame.font.Font(font_style, round(font_size))
    return font_dict[string_hold]

# --- main --- (calling stuff)

# - init -
pygame.init()
info = pygame.display.Info()
pygame.display.set_caption("hex_grid.py")

# - constants - (UPPER_CASE)
if True: # initial screen stuff
    SCREEN_WIDTH,SCREEN_HEIGHT = info.current_w,info.current_h
    EFFECTIVE_SCREEN_HEIGHT = SCREEN_HEIGHT-50

if True: # info bar stuff
    SIDEBAR_LEFT_RATIO = 0.8
    SIDEBAR_LEFT_X = SIDEBAR_LEFT_RATIO*SCREEN_WIDTH
    SCREEN_CENTER_WITH_SIDEBAR = (SIDEBAR_LEFT_X/2, EFFECTIVE_SCREEN_HEIGHT/2)
    ACTION_BAR_TOP_RATIO = 0.8
    ACTION_BAR_TOP_Y = ACTION_BAR_TOP_RATIO*EFFECTIVE_SCREEN_HEIGHT 

if True: # hex stuff
    if True: # hex radius stuff
        HEXMAP_INITIAL_OUTER_RAD = 70
        HEXMAP_INITIAL_INNER_RAD_MODIFIER = 0.85

    if True: # zoom stuff
        HEXMAP_INITIAL_ZOOM_MODIFIER = 1.0
        VAR_ZOOM_MODIFIER = HEXMAP_INITIAL_ZOOM_MODIFIER
        HEXMAP_MIN_ZOOM_MODIFIER = 0.2
        HEXMAP_ZOOM_MODIFIER_INCREMENT = 0.2
        HEXMAP_MAX_ZOOM_MODIFIER = HEXMAP_MIN_ZOOM_MODIFIER + (HEXMAP_ZOOM_MODIFIER_INCREMENT * 20)

if True: # colors
    BLACK = (  0,   0,   0)
    WHITE = (255, 255, 255)
    RED   = (255,   0,   0)
    YELLOW= (255, 234,   0)
    GREEN = (  0, 255,   0)
    GRAY  = (211, 211, 211)

    WHITE_DISABLED = (  0,   0,   1)

    PURPLE_SELECTOR =(218, 112, 214)

    BLUE_LIGHT_GENERIC_WATER = (153, 204, 255)
    GREEN_GENERIC_GRASSLAND  = (  0, 255, 128)
    SAND_YELLOW_DESERT       = (255, 241, 165)

    TERRAIN_COLORS_DICT = {"desert":SAND_YELLOW_DESERT, 
                           "undetermined":RED, 
                           "generic_water":BLUE_LIGHT_GENERIC_WATER, 
                           "generic_grassland":GREEN_GENERIC_GRASSLAND}

if True: # misc
    FPS = 60

if True: # hexmap draw limits
    HEXMAP_DRAW_MIN_X = 0
    HEXMAP_DRAW_MAX_X = SCREEN_WIDTH
    HEXMAP_DRAW_MIN_Y = 0
    HEXMAP_DRAW_MAX_Y = EFFECTIVE_SCREEN_HEIGHT
    pass

# - objects - 
screen = pygame.display.set_mode([SCREEN_WIDTH, EFFECTIVE_SCREEN_HEIGHT], pygame.RESIZABLE)
clock = pygame.time.Clock()

font_dict = {}

hex_grid = HexGrid(20, 15)

if True: # creating rects/surfaces for hexes
    hex_process_tracker = list(hex_grid.hex_dict.values())
    process_tracker_max = len(hex_process_tracker) 
    for hex in hex_grid.hex_dict.values():
        print(f"processing hex {hex_process_tracker.index(hex)+1}/{process_tracker_max}")
        rect_surface_dict = hex.data["hex_rects/surfaces_dict"]

        zoom_basehex_dict = {}
        zoom = HEXMAP_MIN_ZOOM_MODIFIER
        while zoom <= HEXMAP_MAX_ZOOM_MODIFIER:
            outer_values_dict = generate_hex_points_from_center((0,0), HEXMAP_INITIAL_OUTER_RAD*zoom)
            inner_values_dict = generate_hex_points_from_center((0,0), HEXMAP_INITIAL_OUTER_RAD*zoom*HEXMAP_INITIAL_INNER_RAD_MODIFIER)
            zoom_basehex_dict[zoom] = {"base_outer_hex":pygame.draw.polygon(screen, BLACK, list(outer_values_dict.values()))} # create ref hex
            zoom_basehex_dict[zoom][f"base_inner_hex_color_{hex.data['primary_terrain']}"] = pygame.draw.polygon(screen, TERRAIN_COLORS_DICT[hex.data['primary_terrain']], list(inner_values_dict.values()))
            #zoom_basehex_dict[zoom]
            zoom += HEXMAP_ZOOM_MODIFIER_INCREMENT

        for zoom in zoom_basehex_dict.keys():
            dummy_key = list(zoom_basehex_dict[zoom].keys())[0]
            print(dummy_key)
            dummy_surface = pygame.Surface((zoom_basehex_dict[zoom][dummy_key].width *2, zoom_basehex_dict[zoom][dummy_key].height *2)) # create surface from ref hex
            #dummy_surface = pygame.Surface((70, 70))
            #print(f"zoom:{zoom}/{zoom_basehex_dict[zoom][dummy_key].width},{zoom_basehex_dict[zoom][dummy_key].height}")
            dummy_surface_center = (dummy_surface.get_width()/2, dummy_surface.get_height()/2) # get center coords of hex ref surface
            outer_dummy_dict = generate_hex_points_from_center(dummy_surface_center, HEXMAP_INITIAL_OUTER_RAD*zoom) # get outer hex points based on hrs center coord
            inner_dummy_dict = generate_hex_points_from_center(dummy_surface_center, HEXMAP_INITIAL_OUTER_RAD*zoom*HEXMAP_INITIAL_INNER_RAD_MODIFIER) # get inner hex points based on hrs center coord



            key_list = list(zoom_basehex_dict[zoom].keys())
            rect_surface_dict[zoom] = {"surface":{"main":dummy_surface, 
                                                  "label": getFont(12*zoom).render(f"{hex.id}", True, "black", "white")
                                                  }
                                       }
            rect_surface_dict[zoom]["surface"]["main"].fill(WHITE_DISABLED) # fill hex ref surface
            rect_surface_dict[zoom]["surface"]["main"].set_colorkey(WHITE_DISABLED) # transparentize hex ref surface
            rect_surface_dict[zoom]["rects"] = {"outer_hex_rect":pygame.draw.polygon(rect_surface_dict[zoom]["surface"]["main"], BLACK, list(outer_dummy_dict.values())), 
                                                "inner_hex_rect":pygame.draw.polygon(rect_surface_dict[zoom]["surface"]["main"], TERRAIN_COLORS_DICT[hex.data['primary_terrain']], list(inner_dummy_dict.values())), 
                                                "surface_rect":rect_surface_dict[zoom]["surface"]["main"].get_rect(), 
                                                "label_rect":rect_surface_dict[zoom]["surface"]["label"].get_rect()
                                                }
            rect_surface_dict[zoom]["rects"]["label_rect"].center = dummy_surface_center
            
            pass

        pass

    pass

if True: # creating selector hex border
    selector_hex_dict = {}

    zoom_basehex_dict = {}
    zoom = HEXMAP_MIN_ZOOM_MODIFIER
    while zoom <= HEXMAP_MAX_ZOOM_MODIFIER:
            outer_values_dict = generate_hex_points_from_center((0,0), HEXMAP_INITIAL_OUTER_RAD*zoom*1.05)
            inner_values_dict = generate_hex_points_from_center((0,0), HEXMAP_INITIAL_OUTER_RAD*zoom*HEXMAP_INITIAL_INNER_RAD_MODIFIER*0.95)
            zoom_basehex_dict[zoom] = {"base_outer_hex":pygame.draw.polygon(screen, PURPLE_SELECTOR, list(outer_values_dict.values()))} # create ref hex
            zoom_basehex_dict[zoom][f"base_inner_hex_color_transparent"] = pygame.draw.polygon(screen, WHITE_DISABLED, list(inner_values_dict.values()))
            zoom += HEXMAP_ZOOM_MODIFIER_INCREMENT

    for zoom in zoom_basehex_dict.keys():
            dummy_key = list(zoom_basehex_dict[zoom].keys())[0]
            print(dummy_key)
            dummy_surface = pygame.Surface((zoom_basehex_dict[zoom][dummy_key].width *2, zoom_basehex_dict[zoom][dummy_key].height *2)) # create surface from ref hex
            #dummy_surface = pygame.Surface((70, 70))
            #print(f"zoom:{zoom}/{zoom_basehex_dict[zoom][dummy_key].width},{zoom_basehex_dict[zoom][dummy_key].height}")
            dummy_surface_center = (dummy_surface.get_width()/2, dummy_surface.get_height()/2) # get center coords of hex ref surface
            outer_dummy_dict = generate_hex_points_from_center(dummy_surface_center, HEXMAP_INITIAL_OUTER_RAD*zoom*1.05) # get outer hex points based on hrs center coord
            inner_dummy_dict = generate_hex_points_from_center(dummy_surface_center, HEXMAP_INITIAL_OUTER_RAD*zoom*HEXMAP_INITIAL_INNER_RAD_MODIFIER*0.95) # get inner hex points based on hrs center coord



            key_list = list(zoom_basehex_dict[zoom].keys())
            selector_hex_dict[zoom] = {"surface":{"main":dummy_surface, 
                                                  "label": getFont(8*zoom).render(f"", True, "black", "white")
                                                  }
                                       }
            selector_hex_dict[zoom]["surface"]["main"].fill(WHITE_DISABLED) # fill hex ref surface
            selector_hex_dict[zoom]["surface"]["main"].set_colorkey(WHITE_DISABLED) # transparentize hex ref surface
            selector_hex_dict[zoom]["rects"] = {"outer_hex_rect":pygame.draw.polygon(selector_hex_dict[zoom]["surface"]["main"], PURPLE_SELECTOR, list(outer_dummy_dict.values())), 
                                                "inner_hex_rect":pygame.draw.polygon(selector_hex_dict[zoom]["surface"]["main"], WHITE_DISABLED, list(inner_dummy_dict.values())), 
                                                "surface_rect":selector_hex_dict[zoom]["surface"]["main"].get_rect(), 
                                                "label_rect":selector_hex_dict[zoom]["surface"]["label"].get_rect()
                                                }
            selector_hex_dict[zoom]["rects"]["label_rect"].midtop = selector_hex_dict[zoom]["rects"]["outer_hex_rect"].midtop
            
            pass
    
    def blit_select_marker(zoom:float, center:tuple=None):
        global selected_hex
        if center == None:
            center = selected_hex.data["hex_rects/surfaces_dict"][zoom]["rects"]["surface_rect"].center
        selector_hex_dict[zoom]["rects"]["surface_rect"].center = center
        selector_hex_dict[zoom]["surface"]["main"].blit(selector_hex_dict[zoom]["surface"]["label"], selector_hex_dict[zoom]["rects"]["label_rect"])
        screen.blit(selector_hex_dict[zoom]["surface"]["main"], selector_hex_dict[zoom]["rects"]["surface_rect"])
        pass

hex_grid.calculate_centers(outer_rad_input=HEXMAP_INITIAL_OUTER_RAD, # initialize hex centers
                           current_zoom=VAR_ZOOM_MODIFIER, 
                           coord_of_00=None)

selected_hex = hex_grid.hex_dict["0,0"]

# - initial states - (True/False)
running = True

if True: # modes
    mode_hex_map = True
    mode_battle_map = False
    mode_party_info = False
    mode_hex_map_zoomed = False

    hex_map_drag = False

# - stuff -
yes = 0
while running:
    if yes == -1:
        input()
    for event in pygame.event.get(): #event handler
        keys_pressed = pygame.key.get_pressed()
        
        if True: # exit handlers
            if event.type == pygame.QUIT: #exit game
                running = False
            elif event.type == pygame.KEYDOWN:
                if keys_pressed[pygame.K_KP2] and keys_pressed[pygame.K_KP4] and keys_pressed[pygame.K_KP6] and keys_pressed[pygame.K_KP8]: #force exit game
                    running = False

        if mode_hex_map == True: # hex map stuff
            if event.type == pygame.KEYDOWN: # mode switching
                if keys_pressed[pygame.K_LCTRL] and keys_pressed[pygame.K_b]:
                    mode_battle_map = True
                    mode_hex_map = False

                elif keys_pressed[pygame.K_LCTRL] and keys_pressed[pygame.K_c]:
                    mode_party_info = True
                    mode_hex_map = False

                elif keys_pressed[pygame.K_RETURN]:
                    mode_hex_map_zoomed = True
                    mode_hex_map = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    mouse_x, mouse_y = hexdrag_click_origin_x, hexdrag_click_origin_y =  mousex2, mousey2 = event.pos
                    hex_map_drag = True
                
                elif event.button == 1:
                    print("doot")
                    #winsound.Beep(200, 500)
                    eligible_hexes = {}
                    for hex in hex_grid.hex_dict.values():
                        if hex.data["hex_rects/surfaces_dict"][VAR_ZOOM_MODIFIER]["rects"]["surface_rect"].collidepoint(event.pos):
                            eligible_hexes[hex] = sqrt((hex.data["hex_rects/surfaces_dict"][VAR_ZOOM_MODIFIER]["rects"]["surface_rect"].center[0]-event.pos[0])**2 + (hex.data["hex_rects/surfaces_dict"][VAR_ZOOM_MODIFIER]["rects"]["surface_rect"].center[1]-event.pos[1])**2)
                            #winsound.Beep(600, 500)
                    
                    eligible_hexes_list = list(eligible_hexes.keys())
                    for hex in eligible_hexes_list:
                        if eligible_hexes_list.index(hex) != 0:
                            if eligible_hexes[hex] < eligible_hexes[champion_hex]:
                                champion_hex = hex
                        elif eligible_hexes_list.index(hex) == 0:
                            champion_hex = hex
                    
                    selected_hex = champion_hex

                    pass
                
                elif event.button == 4 and keys_pressed[pygame.K_LCTRL]:
                    VAR_ZOOM_MODIFIER += HEXMAP_ZOOM_MODIFIER_INCREMENT
                    if VAR_ZOOM_MODIFIER > HEXMAP_MAX_ZOOM_MODIFIER:
                        VAR_ZOOM_MODIFIER = HEXMAP_MAX_ZOOM_MODIFIER
                    hex_grid.calculate_centers(outer_rad_input=HEXMAP_INITIAL_OUTER_RAD, # initialize hex centers
                                                current_zoom=VAR_ZOOM_MODIFIER, 
                                                coord_of_00=None)
                elif event.button == 5 and keys_pressed[pygame.K_LCTRL]:
                    VAR_ZOOM_MODIFIER -= HEXMAP_ZOOM_MODIFIER_INCREMENT
                    if VAR_ZOOM_MODIFIER < HEXMAP_MIN_ZOOM_MODIFIER:
                        VAR_ZOOM_MODIFIER = HEXMAP_MIN_ZOOM_MODIFIER
                    hex_grid.calculate_centers(outer_rad_input=HEXMAP_INITIAL_OUTER_RAD, # initialize hex centers
                                                current_zoom=VAR_ZOOM_MODIFIER, 
                                                coord_of_00=None)
                pass
            
            elif event.type == pygame.MOUSEMOTION:
                if hex_map_drag == True:
                    mouse_x, mouse_y = event.pos
                    offset_x = mouse_x - mousex2
                    offset_y = mouse_y - mousey2

                    mousex2, mousey2 = event.pos

                    for hex in hex_grid.hex_dict.values():
                        #hex.screen_coord_center = (hex.screen_coord_center[0] + offset_x, hex.screen_coord_center[1] + offset_y)
                        doot = hex.data["hex_rects/surfaces_dict"][VAR_ZOOM_MODIFIER]["rects"]["surface_rect"].center
                        doot2 = (doot[0]+offset_x, doot[1]+offset_y)
                        hex.data["hex_rects/surfaces_dict"][VAR_ZOOM_MODIFIER]["rects"]["surface_rect"].center = doot2
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    hex_map_drag = False
            pass

    # - updates (without draws) - 

    # - draws (without updates) -


    if True: #drawing handler
        screen.fill(GRAY)
        if mode_hex_map == True: #draws for mode: hex map
            screen_center = screen.get_rect().center

            for hex in hex_grid.hex_dict.values():
                if hex.data["hex_rects/surfaces_dict"][VAR_ZOOM_MODIFIER]["rects"]["surface_rect"].center[0] <= HEXMAP_DRAW_MAX_X:
                    if hex.data["hex_rects/surfaces_dict"][VAR_ZOOM_MODIFIER]["rects"]["surface_rect"].center[0] >= HEXMAP_DRAW_MIN_X:
                        if hex.data["hex_rects/surfaces_dict"][VAR_ZOOM_MODIFIER]["rects"]["surface_rect"].center[1] <= HEXMAP_DRAW_MAX_Y:
                            if hex.data["hex_rects/surfaces_dict"][VAR_ZOOM_MODIFIER]["rects"]["surface_rect"].center[1] >= HEXMAP_DRAW_MIN_Y:
                                hex.blit_hex(VAR_ZOOM_MODIFIER)
                            else:pass
                        else:pass
                    else:pass
                else:pass

                pass

            blit_select_marker(VAR_ZOOM_MODIFIER)
            pass

        elif mode_battle_map == True:
            pass

        elif mode_hex_map_zoomed == True:
            pass

        elif mode_party_info == True:
            pass

        pygame.display.flip()
    
    yes +=1
    
    # - constant game speed / FPS -
    clock.tick(FPS)
    

    