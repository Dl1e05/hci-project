### User

UserBase: 
username: str
email: str
birth_date: date

UserCreate(UserBase):
password: str
password_repeat: str

UserRead(UserRead):
id: UUID
is_active: bool


### ContentType

ContentTypeBase:
name: str
order: positiveint
tags: m2m

ContentTypeCreate(ContentTypeBase):

ContentTypeRead(ContentTypeBase):
id: UUID

### Tags

TagsBase:
name: str 
code: str

TagsCreate(TagsBase):

TagsRead(TagsBase):
id: UUID



