1.非数字主键必须带参数save

https://docs.peewee-orm.com/en/latest/peewee/models.html#id4

Auto-incrementing IDs are, as their name says, automatically generated for you when you insert a new row into the database. When you call save(), peewee determines whether to do an INSERT versus an UPDATE based on the presence of a primary key value. Since, with our uuid example, the database driver won’t generate a new ID, we need to specify it manually. When we call save() for the first time, pass in force_insert = True:

# This works because .create() will specify `force_insert=True`.
obj1 = UUIDModel.create(id=uuid.uuid4())

# This will not work, however. Peewee will attempt to do an update:
obj2 = UUIDModel(id=uuid.uuid4())
obj2.save() # WRONG

obj2.save(force_insert=True) # CORRECT

# Once the object has been created, you can call save() normally.
obj2.save()