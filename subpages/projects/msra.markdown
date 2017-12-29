---
layout: detail
---

### Pixel-level prediction for multiple tasks

People have already found that transfer learning accelerates learning process compared to learning from scratch. In addition, jointly learning multiple tasks could also be benefit to learning efficiency and quality. Humans are extremely good at transferring knowledge from one task to another. For example, we segment visual image not only based on color, texture and shape information, but also based on depth, movements and semantic clues. Multi-task learning could alleviate the heavy reliance on labeled data by using internal intrinsic signals like consistency and predictability between tasks.

The following structure is designed for stereo matching. This network was trained on Sceneflow dataset and finetuned on KITTI dataset. 

![structure]({{ site.baseurl }}/image/cnn_structure.jpg){: .centerimg}

Here are some of the results on KITTI dataset.

<video id="video" controls="" preload="none" poster="{{ site.baseurl }}/image/kitti-17.png">
      <source id="mp4" src="{{ site.baseurl }}/video/driving.mp4" type="video/mp4">
      <p>Your user agent does not support the HTML5 Video element.</p>
</video>
