from simple_image_download import simple_image_download as simp



if __name__ == "__main__":
    response = simp.simple_image_download

    response().download('thai chilli', 5)

    print(response().urls('thai chilli', 5))