from typing import Any, Dict, List, Optional


class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[List[Any]] = None,
        props: Optional[Dict[str, str]] = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ""
        return " " + " ".join(map(lambda x: f'{x[0]}="{x[1]}"', self.props.items()))

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: Optional[str],
        value: str,
        props: Optional[Dict[str, str]] = None,
    ) -> None:
        super().__init__(tag, value, props=props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
