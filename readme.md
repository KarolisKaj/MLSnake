# ML with snake game

Create model to play snake game.

TODO:
* Gather training data +
* Fix data +
* Start over gathering data
* Use model for snake
* Allow snake to play and gather more proper data.
* Let it play & win :)

# Change log:
1. Seperate decisions into two different models;
   1. Make model for clasification whether direction must change on this step;
   2. Another model to decide which direction to take if first model returns true;
      1. Direction model only trains on data which actually changed direction

Flaws:
* Data was incorrect