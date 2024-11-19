class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        
        html = ""
        for prop in self.props:
            html += f' {prop}="{self.props[prop]}"'

        return html
    
    def __repr__(self):
        repr = f"HTMLNode({self.tag}, {self.value}"

        if self.children != None:
            repr += ","
            for child in self.children:
                repr += f" {child}"
        else:
            repr += ", no children"

        if self.props != None:
            dict_string = ""
            for prop in self.props:
                dict_string += f"{prop}: {self.props[prop]}, "
            repr += f", {{{dict_string.rstrip(", ")}}}"
        else:
            repr += ", no props"

        repr += ")"
        
        return repr