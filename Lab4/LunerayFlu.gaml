/**
 *  Lab4
 *  Author: Rahul Kothuri, Isak Nyberg
 *  Description: Lunerays Flu Modelling
 */

model Lab4

/* Insert your model definition here */
global {
    int nb_people <- 2147;// The given population of Luneray
    int nb_infected_init <- 5;// The number of people that are intially infected 
    float step <- 5 #mn;// The simulation step
	
	// The number of people infected starts at 5 and is updated constantly by using update
    int nb_people_infected <- nb_infected_init update: people count (each.is_infected);
    // The number of people who are not infected is given by total number of people - number of infected people
    int nb_people_not_infected <- nb_people - nb_infected_init update: nb_people - nb_people_infected;
    // The rate of infection
    float infected_rate update: nb_people_infected/nb_people;
    
    file road_shapes <- file("../includes/roads.shp");// Shapefile for the roads
    file building_shapes <- file("../includes/buildings.shp");// Shape file for the buildings
    geometry shape <- envelope(road_shapes); //The shape is defined as an envelop of the road_shapes file
    graph road_network;// The road network for the city instantiated here
	
    init{
    // The people are created to be used in the map
	create people number:nb_people;
	// The roads are created from the shapefile
	create road from: road_shapes;
	// The as_edge_graph here creates a graph from a set of polylines
	road_network <- as_edge_graph(road); 
	// The buildings are created from the shapefile
	create building from: building_shapes;
	// If the intial infected people are among the others, then they are also infected
	ask nb_infected_init among people {
	    is_infected <- true;
	}
  }
	// This ends the simulation when everyone is infected
    reflex end_simulation when: infected_rate = 1.0 {
	      do pause;
    }	
}
// The people are defined here as being only able to move
species people skills:[moving]{	
	// The speed is given as 2-5 kmph	
    float speed <- (2 + rnd(3)) #km/#h;
    // Intially apart from the 5, the other people are not infected
    bool is_infected <- false;
    // Target is the location of a person's destination represented by a point
    point target;
    // The 3D representation of people for the 3D Map
    aspect geom3D{
    	if target != nil{// If the agent is not in the house
    		draw obj_file("../includes/people.obj",90::{-1,0,0}) size: 10// The people are drawn here
    		  at: location + {0,0,7} rotate: heading - 90 color: is_infected ? #red : #green;
    	}
    }
    // This is activated when the agent is in the house and using the probabaility of 0.05 whether the agent
    // has to go out or not
    reflex stay when: target = nil{
    	if flip(0.05){
    		target <- any_location_in(one_of(building));// Goes to a random destination
    	}
    }
	// This is activated when the agent is not at home and has to go back home
    reflex move when: target != nil{
    	do goto target: target on: road_network;
    	if(location = target){
    		target <- nil;
    	}
    }
    // If the distance is less than or equal to 10m then is_infected is true
    reflex infect when: is_infected{
	ask people at_distance 10 #m {
	    if flip(0.05) {
		is_infected <- true;
	    }
	}
  }
	// For the 2D map we represent people as circles
    aspect circle {
	draw circle(10) color:is_infected ? #red : #green;
    }
}
// This is how the 2D roads are defined here
species road{
	aspect geom{
		draw shape color: #black;// The color of the roads are black
	}
	// This is the 3D version of the roads
	 aspect geom3D {
	draw line(shape.points, 2.0) color: #black;
    }
} 
// This represents the building on the map
species building{
	// The 2D representation of the building
	aspect geom{
		draw shape color: #gray;// The buildings are gray in color
	}
	// The 3D version of the building along with the picture and the texture
	aspect geom3D {
	    draw shape depth: 20 #m border: #black texture: ["../includes/roof_top.png","../includes/texture.jpg"];
    }
}
// The experimentation part which is used to model the spreading of the flu virus
experiment main type: gui {
    parameter "Nb people infected at init" var: nb_infected_init min: 1 max: 2147;

    output {
	monitor "Infected people rate" value: infected_rate;
	// The 2D map that is being created to show the spread of the virus
	display map type:opengl{
		species road aspect: geom;
	    species building aspect: geom;
	    species people aspect: circle;
	}
	// The chart that shows the relation between the number of healthy and infected people
	// It is refreshes every 10 cycles to update the results
	display chart refresh: every(10 #cycles) {
	    chart "Disease spreading" type: series {
		data "susceptible" value: nb_people_not_infected color: #green;
		data "infected" value: nb_people_infected color: #red;
	    }
	}
	// This is the 3D version of the map that shows the spread of the virus
	// Here we use the Luneray map for the roads and buildings
    display view3D type: opengl ambient_light:80{
    	 image "../includes/luneray.png" refresh: false; 
	     species building aspect: geom3D refresh: false;
	     species road aspect: geom3D refresh: false;
	     species people aspect: geom3D; 
    }
  }
}
