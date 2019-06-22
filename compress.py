import importlib
import dct
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.dpi'] = 180
import imageio
import math

def remove_frequencies(frequencies, d):
    freq_h = frequencies.shape[0]
    freq_w = frequencies.shape[1]
    final_frequencies = np.zeros(frequencies.shape)

    for i in range(min(freq_h, d)):
        for j in range(min(freq_w, d)):
            if i+j < d:
                final_frequencies[i][j] = frequencies[i][j]
    return final_frequencies

def compress(image, F, D):
    image_width = image.shape[0]
    image_height = image.shape[1]
    hor_chunks = math.ceil(image_width / F)
    ver_chunks = math.ceil(image_height / F)

    compressed_image = image.copy()
    for h in range(hor_chunks):
        for v in range(ver_chunks):
            submatrix = image[h*F:min((h+1)*F, image_width), v*F:min((v+1)*F, image_height)]
            #print(submatrix)
            frequencies_matrix = dct.fdct2t(submatrix)
            #print(frequencies_matrix)
            removed_frequencies = remove_frequencies(frequencies_matrix, D)
            #print(removed_frequencies)
            inverted_frequencies = dct.ifdct2t(removed_frequencies)
            inverted_frequencies = np.rint(inverted_frequencies).astype(int)
            inverted_frequencies = np.clip(inverted_frequencies, 0, 255)
            #print(inverted_frequencies)
            compressed_image[h*F:min((h+1)*F, image_width), v*F:min((v+1)*F, image_height)] = inverted_frequencies
            #print(compressed_image)
            #break
        #break
    
    return compressed_image

def do_compress(FILEPATH, F, D):
    image = imageio.imread(FILEPATH)
    if len(image.shape) is 3:
        image = image[:,:,0]
    
    compressed_image = compress(image, F, D)

    subplots = [121, 122]

    ax1 = plt.subplot(subplots[0])
    plt.imshow(image, cmap='gray', vmin=0, vmax=255)
    plt.title("Original")
    ax1.tick_params(labelbottom=False, labeltop=False, labelleft=False, labelright=False, bottom=False, top=False, left=False, right=False)
    ax1.spines['bottom'].set_color('blue')
    ax1.spines['top'].set_color('blue') 
    ax1.spines['right'].set_color('blue')
    ax1.spines['left'].set_color('blue')
    
    ax2 = plt.subplot(subplots[1], sharex=ax1, sharey=ax1)
    plt.title(f"Compressed\nF: {F} - D: {D}")
    plt.imshow(compressed_image, cmap='gray', vmin=0, vmax=255)
    ax2.tick_params(labelbottom=False, labeltop=False, labelleft=False, labelright=False, bottom=False, top=False, left=False, right=False)
    ax2.spines['bottom'].set_color('blue')
    ax2.spines['top'].set_color('blue') 
    ax2.spines['right'].set_color('blue')
    ax2.spines['left'].set_color('blue')



    return plt.show()
