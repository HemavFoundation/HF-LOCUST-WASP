global connectionString
global typeOfMission
global inverse
global visual_camera_settings, monospectral_camera_settings, flight_controller


drone_id = 'HP2-087'

connectionString = "drone" # 'local' for testing in localhost // 'drone' for testing in the raspi
typeOfMission = "straight" # periscope, straight, rectangle, zigzag
inverse = False

visual_camera_settings = dict(
    port = '/dev/video1',
    frame_width = 3264, 
    frame_height = 2448,
    auto_exposure = 3,
    brightness = -10,
    contrast = 0,
    saturation = 52,
    light_compensation = 1,
    white_balance = 4600,
    gamma = 160,
    sharpness = 3,
    fps = 10,
    timer = 30, # Timer in seconds to trigger the camera
)

monospectral_camera_settings = dict(
    frame_width = 2528, 
    frame_height = 1968,
    redAWB = 0.9,
    blueAWB = 2.2,
    awb_mode = 'off',
    brightness = 30,
    exposure_mode = 'auto',
    drc_strength = 'high',
    timer = 6, 
)

flight_controller = dict(
    port = '/dev/serial0',
    baudrate = 921600,
)

rockblock_settings = dict(
    port = '/dev/ttyUSB0',
    baudrate = 19200,
    message_timer = 120, # Send message timer in seconds
)

mission_settings = dict(
    
)

