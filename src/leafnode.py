from htmlnode import *

class LeafNode(HTMLNode):
    def __init__(self, value, tag = None, props = None):
        super().__init__(value = value, tag = tag, props = props)

    def to_html(self):
        # print(self)
        
        if self.value == None:
            raise ValueError
        
        if self.tag == None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
