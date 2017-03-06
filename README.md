Testing how far I can push flattening an alLayer shader into one single alSurface shader.

In many occasions I tend to build layered shading networks which don't actually need to be layered, it is just easier to build them that way. This little script will aim to flatten the layered shader into a single surface shader.

Ofcourse many great features of layered bxdfs will be thrown away, such as layered brdfs, etc. Alsurface also doesn't allow mapping of the IOR modes, so it can't work for layered shaders which combine dialectric/metallic IOR modes. Stick to the good stuff if you're building complex shader networks and forget about this ;)