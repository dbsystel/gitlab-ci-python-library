from gcip import Image


def test_image_class_only_with_image():
    image = Image("alpine:3")
    assert image.name == "alpine:3"
    assert image.entrypoint is None
    assert image.render() == {"name": "alpine:3"}


def test_image_class_with_entrypoint():
    image = Image("alpine:3", entrypoint=["/bin/sh", "-c", "cat", "/etc/os-release"])
    assert image.name == "alpine:3"
    assert image.entrypoint == ["/bin/sh", "-c", "cat", "/etc/os-release"]
    assert image.render() == {"name": "alpine:3", "entrypoint": ["/bin/sh", "-c", "cat", "/etc/os-release"]}
