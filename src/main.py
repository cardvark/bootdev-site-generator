from textnode import TextType
from textnode import TextNode


def main():
    text_obj = TextNode("some text", TextType.LINK, "www.fakeurl.com")
    print(text_obj)

main()