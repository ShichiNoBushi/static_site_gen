from htmlnode import *
from leafnode import *

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag = tag, children = children, props = props)

    def to_html(self):
        # print(self)
        
        if self.tag == None:
            raise ValueError("Node has no tag.")
        
        if self.children == None or len(self.children) == 0:
            raise ValueError("Node has no children.")
        
        html = f"<{self.tag}{self.props_to_html()}>"

        for child in self.children:
            html += child.to_html()

        html += f"</{self.tag}>"
        return html