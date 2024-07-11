import math;
def reward_function(params):
    '''
    Example of rewarding the agent to follow center line
    '''
    
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    all_wheels_on_track = params['all_wheels_on_track']
    abs_steering = abs(params['steering_angle'])
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    speed = params['speed']
    
    #Set the speed threshold based your action space
    SPEED_THRESHOLD = 1.0

    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.2 * track_width
    marker_3 = 0.3 * track_width
    marker_4 = 0.4 * track_width
    marker_5 = 0.5 * track_width
    
    if not all_wheels_on_track:
        reward = 1e-3
        return float(reward)
    
    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 3.0
    elif distance_from_center <= marker_2:
        reward = 2.5
    elif distance_from_center <= marker_3:
        reward = 1.5
    elif distance_from_center <= marker_4:
        reward = 1.0
    elif distance_from_center <= marker_5:
        reward = 0.5
    else:
        reward = 1e-3  # likely crashed/ close to off track
        return float(reward)
    
    if not all_wheels_on_track:
        # Penalize if the car goes off track
        reward = 1e-3
        return float(reward)
    elif speed < SPEED_THRESHOLD:
        # Penalize if the car goes too slow
        reward = reward * 0.8
    else:
        # High reward if the car stays on track and goes fast
        reward += 1.0
        
    # Give a high reward if no wheels go off the track and 
    # the car is somewhere in between the track borders 
    if all_wheels_on_track and (0.5*track_width - distance_from_center) >= 0.05:
        reward += 1.0

    #Steering penality threshold, change the number based on your action space setting
    ABS_STEERING_THRESHOLD = 20

    # Penalize reward if the car is steering too much
    if abs_steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8
        
    #Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    # Convert to degree
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    # Penalize the reward if the difference is too large
    DIRECTION_THRESHOLD = 10.0
    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.5
    
    return float(reward)