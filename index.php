<?php

// Include your model and controller classes
require './models/PostModel.php';
require './controllers/PostController.php';

// Instantiate the controller
$postController = new PostController();

// Call the index method
$postController->index();
