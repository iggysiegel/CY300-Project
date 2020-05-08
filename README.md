# CY300-Project

"Cadet vs. Covid" is a side-scrolling dungeon game. The player uses the arrow keys to
move an avatar across the level; each level represents one floor of Davis barracks.
While in the hallway, players must jump to avoid the airborne coronavirus particles.
One each floor there are several doors that players can choose to enter; each room
randomly contains either CGR, medical supplies, or both. Medical supplies (washing hands)
increases the player's health, giving them more times they can be hit by coronavirus before
becoming infected and losing. Running into CGR forces players to act fast to
avoid mandatory Commadant's PT (health penalty). At the end of each level, players enter a
final door that takes them to the next level, where the enemies are faster.

Currently, the code displays a basic start screen and a rough initial level. The variables
necessary to play are game_status (which tells the loop what to show), the timer (which
corresponds to score), health (which is the amount of lives left), and a few others that
support movement around the screen. Future additions will include the ability to transition
from the hallway (game state 2) to a room (game state 3) to interact with the enemies and a
method of increasing the difficulty to match the level.

The project team includes CDTs Siegel and Bolen. We use the modules pygame, pgzrun, and random.
