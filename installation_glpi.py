import apt

# First of all, open the cache
cache = apt.Cache()
# Now, lets update the package list
cache.update()
# We need to re-open the cache because it needs to read the package list
cache.open(None)
# Now we can do the same as 'apt-get upgrade' does
cache.upgrade()
# or we can play 'apt-get dist-upgrade'
cache.upgrade(True)
# Q: Why does nothing happen?
# A: You forgot to call commit()!
cache.commit()
