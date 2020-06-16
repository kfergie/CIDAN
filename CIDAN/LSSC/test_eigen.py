import matplotlib.pyplot as plt
from dask import compute
from scipy.sparse import csr_matrix

from CIDAN.LSSC.functions.data_manipulation import *
from CIDAN.LSSC.functions.eigen import *


def test_eigen():
    shape = (200, 200)
    num_points = 15
    shape_2d = (num_points * 25, 2)
    save_dir = "/Users/sschickler/Code Devel/LSSC-python/input_images/test2"
    image = np.zeros(shape_2d, dtype=np.float)
    for i in range(0, num_points, 1):
        for j in range(0, 25, 1):
            image[i * 25 + j, 0] = i
            image[i * 25 + j, 1] = j

    num_eig = 50
    # image_2d = reshape_to_2d_over_time(np.transpose(image,(2,0,1)))
    # K = calcAffinityMatrix(pixel_list=image, metric="l2", knn=20,
    #                        accuracy=80, connections=30,
    #                        normalize_w_k=15, num_threads=8, spatial_box_num=0,
    #                        temporal_box_num=0).compute()
    K_new = np.zeros((15 * 25, 15 * 25))
    for i in range(0, num_points, 1):
        for j in range(0, 25, 1):
            if (i > 0):
                K_new[i * 25 + j, (i - 1) * 25 + j] = 1
            if (i < num_points - 1):
                K_new[i * 25 + j, (i + 1) * 25 + j] = 1
            if (j > 0):
                K_new[i * 25 + j, (i) * 25 + j - 1] = 1
            if (j < 25 - 1):
                K_new[i * 25 + j, (i) * 25 + j + 1] = 1

    e_vectors = generateEigenVectors(K=csr_matrix(K_new), num_eig=num_eig)
    e_vectors = np.array(compute(e_vectors)[0])
    # plt.pcolormesh(e_vectors.transpose((1,0)))
    num = 0
    print(np.max(e_vectors[:, num]), np.min(e_vectors[:, num]))
    plt.scatter(image.transpose((1, 0))[0], image.transpose((1, 0))[1],
                c=e_vectors[:, num])
    plt.show()
    # save_image(image[:,:,0],0,shape,save_dir)
    # for x in range(num_eig):
    #     save_image(e_vectors[:, x], x + 1, shape, save_dir)


def save_image(image, num, shape, save_dir):
    e_vectors_sum_rescaled = image * (
            10.0 / image.max())  # add histogram equalization

    img = Image.fromarray(
        np.reshape(e_vectors_sum_rescaled,
                   shape) * 255).convert('L')
    image_path = os.path.join(save_dir, "eigen{}.png".format(
        num))
    img.save(image_path)


test_eigen()
