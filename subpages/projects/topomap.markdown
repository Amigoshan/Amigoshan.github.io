---
layout: detail
---
### Auto-Creation and Navigation of the Multi-area Topological Map for 3D Large-scale Environment

Mapping is a critical technology for robot navigation. In the large-scale environment, the topological map is widely used. This study presents a new structure of the topological map with multi-area feature, as well as an approach to use it in navigation. 

![structure]({{ site.baseurl }}/image/topomap_structure.jpg){: .centerimg}

Different floors, different rooms can be divided into different areas. Each area can be regarded as an independent topological map. At the same time, each area is also connected by the special topological link based on actual situation. Usually the connection between two areas are likely to be the elevator between different floors and the passage between different rooms.

![multifloor]({{ site.baseurl }}/image/topomap_multifloor.png){: .centerimg}


The proposed topological map can better represent the large-scale environment with certain features, such multi-room, multi-floor and multi-type. Navigation based on this multi-area topological map is more efficient. The creation and maintenance of the new map is more convenient. 

An algorithm of auto-creating the map has been proposed. Firstly, the data from the Laser Range Finder sensor is converted into a grid map. Secondly, the skeleton of the free space of the map is extracted using graphic algorithms. Finally, critical topological nodes are generated on the skeleton and form a topological map. 

![create]({{ site.baseurl }}/image/topomap_create.png){: .centerimg}
