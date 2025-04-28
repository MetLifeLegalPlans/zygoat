# Please read this page in the [API documentation](https://) instead for reference links + type annotations

This module defines the `Resources` class, which is used to copy files and directories stored in `zygoat` to the generated project.

## Where are files copied from?

Files are copied relative to the `zygoat/resources` directory, which is where all static file resources reside. For instance,

```py
>>> resources = Resources("/home/user/my-project")
>>> resources.cp("backend/Dockerfile")
```

copies `zygoat/resources/backend/Dockerfile` to `/home/user/my-project/backend/Dockerfile`.

You can override the destination path if you wish to structure the internal resource package differently than the resulting project layout, though _this is discouraged_ as it makes the purpose of the resource file less clear at a glance. This is accomplished with the `dest` parameter - to continue our example from earlier, this:

```py
>>> resources.cp("backend/Dockerfile", dest="backend/Dockerfile.bak")
```

copies `zygoat/resources/backend/Dockerfile` to `/home/user/my-project/backend/Dockerfile.bak`.

See `Resources` below for more information.
