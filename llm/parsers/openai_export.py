import json
from typing import List, Dict, Optional, Union
from pydantic import BaseModel

class ImageMetadata(BaseModel):
    content_type: str
    asset_pointer: str
    size_bytes: int
    width: int
    height: int
    fovea: Union[str, None]
    metadata: dict

class MessageContent(BaseModel):
    parts: Union[list[str], list[ImageMetadata]]

class MessageThoughts(BaseModel):
    content_type: str
    content: Optional[str] = None
    thoughts: Optional[list] = None
    source_analysis_msg_id: Optional[str] = None

class MessageAuthor(BaseModel):
    role: str

class Message(BaseModel):
    content: Union[MessageContent, MessageThoughts]
    author: MessageAuthor


class MappingNode(BaseModel):
    id: str
    message: Union[None, Message]
    parent: Optional[str]
    children: List[str]


class ConversationItem(BaseModel):
    title: str
    create_time: float
    update_time: float
    mapping: Dict[str, MappingNode]
    moderation_results: List
    current_node: str
    plugin_ids: Optional[Union[str, None]]
    conversation_id: str
    conversation_template_id: Optional[Union[str, None]]
    gizmo_id: Optional[Union[str, None]]
    gizmo_type: Optional[Union[str, None]]
    is_archived: bool
    is_starred: Optional[Union[bool, None]]
    safe_urls: List
    blocked_urls: List
    default_model_slug: Optional[Union[str, None]]
    conversation_origin: Optional[Union[str, None]]
    voice: Optional[Union[str, None]]
    async_status: Optional[Union[int, None]] = None
    disabled_tool_ids: List
    is_do_not_remember: Optional[Union[bool, None]]
    memory_scope: str
    id: str

class ShapeException(Exception):
    ...

def parse_conversation(mapping: Dict[str, MappingNode]) -> List[Dict[str, Union[str, List[str]]]]:
    conversation = []
    # Open ai seems to inject this...but inconsistently. NOt all convos have them? Why?
    current_id = "client-created-root"
    if current_id not in mapping:
        root = [k for k, v in mapping.items() if v.message is None]
        if len(root) != 1:
            raise ShapeException("OpenAI Conversation was not expected shape. Could not find root to thread convo.")
        current_id = root[0]
 
    while current_id in mapping:
        node = mapping[current_id]
        author_role = node.message.author.role if node.message else ""
        content_parts = node.message.content.parts if node.message else ""
        conversation.append({
            "role": author_role,
            "content": content_parts
        })
        if not node.children:
            break
        # is there ever more than one child and why? 
        current_id = node.children[0]

    return conversation


def load_and_parse_json(file_path: str, item_index: int = 0) -> List[Dict[str, Union[str, List[str]]]]:
    with open(file_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    items = []
    for item in raw_data:
        items.append(ConversationItem.model_validate(item))

    if not (0 <= item_index < len(items)):
        raise IndexError(f"item_index {item_index} out of range (0 to {len(items)-1})")

    selected_item = items[item_index]
    return parse_conversation(selected_item.mapping)


# Example usage:
for item_index in range(500):
    if item_index not in [5, 10, 12, 30]:
        with open(f"conversations/outputs/conversation_output_{item_index}.txt", 'a') as f:
            conversation = load_and_parse_json("conversations/conversations.json", item_index=item_index)
            for turn in conversation:
                f.write(f"\n- {turn['role']}: \n{' '.join(turn['content'])}")
