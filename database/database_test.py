from database import database_objects

# Create your DB object
md = database_objects.Users('md', 'mdrizzle', 'm@mdogy.net', 22, '07/30/1993', 30)

# Save the object, preferably just call the __unicode__ property as the save filename
database_objects.save_object(md, md.__unicode__)

# Let's retrieve it
is_this_md = database_objects.load_object('md')
print is_this_md.username

