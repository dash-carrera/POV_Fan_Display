import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


image_name = 'Circle.png'

def get_polar_coordinates(x, y):
    # Given an x,y coordinate pair, output the coordinates in percent polar coordinates
    # (percent_around_circle, radius)
    r = np.sqrt(pow(x, 2)+pow(y, 2))
    theta = np.arctan2(y, x)
    percent_around_circle = (theta+np.pi)/(2*np.pi)
    return percent_around_circle, r

def downsample_image_to_polar(image_path, num_sections=360, radius=36):
    # Open the image
    image = Image.open(image_path)
    resized_image = image.resize((49, 49), Image.LANCZOS)
    resized_image.save('resized_image.png')
    # Convert the image to a numpy array
    img_array = np.array(resized_image)

    print(img_array)
    rgb_arr = img_array[:, :, :3] #Remove alpha channel if present

    rgb_arr = rgb_arr[np.count_nonzero(rgb_arr == 0, axis=2) != 3]




    sections = []
    debugging_plot_theta = []
    debugging_plot_r = []
    debugging_plot_colors = []

    for i in range(num_sections): #Iterating through each degree
        section = []
        start_percent = i / num_sections
        end_percent = (i + 1) / num_sections
        for x in np.arange(49): #Go over the entire image
            for y in np.arange(49):
                percent_around_circle, r = get_polar_coordinates(x - 24, 24 - y) #Get the polar coordinates
                if percent_around_circle >= start_percent and percent_around_circle < end_percent: #If a pixel is at this degree
                    section += [np.floor(r) + 36] + rgb_arr[x, y].tolist() #Second half of LED strip
                    debugging_plot_theta.append(percent_around_circle * 2 * np.pi + np.pi/2)
                    debugging_plot_r.append(np.floor(r))
                    debugging_plot_colors.append(rgb_arr[x,y]/255)
        section.append(-1)
        sections.append(section)

    #Generate rendered polar image for debugging
    fig = plt.figure()
    ax = fig.add_subplot(projection='polar')
    print(debugging_plot_colors)
    c = ax.scatter(debugging_plot_theta, debugging_plot_r, c = debugging_plot_colors)
    plt.show()


    #Add opposite angled for double rendering to first half of LED strip
    # doubled_sections = []
    # for i, section in enumerate(sections):
    #     opposite_section = sections[int((i+num_sections/2) % 360)] # The opposite section
    #     opposite_section = [(rgb, 71-r) for rgb, r in opposite_section]
    #     doubled_sections.append(section + opposite_section)
    # return doubled_sections

    return sections


# Example usage
sections = downsample_image_to_polar(image_name, num_sections=360, radius=36)
# print(sections)


with open('./image.h', 'w') as f: 
    f.write('const float image[360][290] ICACHE_FLASH_ATTR = {\n');
    f.write(str(sections).replace("[","{").replace("]","},\n")) 
    f.write(';')



