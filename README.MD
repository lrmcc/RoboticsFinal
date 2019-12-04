Robotics Final
Final Test Plans for Parrot BeBop 2

***********************************
          How to Test
***********************************
We plan to have a path of post-it notes along the ground
that our Parrot BeBop 2 will be able to follow. We will test
the algorithm for processing the image that the Parrot finds
and its ability to understand and move to the found post-it.
Once parrot is at the end of the path Parrot should land on the final post-it
and shut down.


***********************************
            Procedure
***********************************
for color processing:
green->go
red->stop/shutdown


Start: lift off to 5 feet

Begin to search to green post-its.
if (!Found){
  move spin
}
else{
  process image
  move to post-it
  stop above post-it
  mask out the new start position
  find the next post-it
}
if(found == red post-it){
  start landing process.
  once landed, shutdown
}
else{
  keep spinning
}
