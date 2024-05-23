# AlbumRater

### [Video Demo](https://youtu.be/2bhyUEy_2qM)

## Overview
Lately I've been getting into listening to albums all the way through, as experiences rather than just separate songs. Tired of trying to keep track of the albums I've listened to in a boring and visually unsatisfying notes app entry, I decided to create this web app as a way to keep track of the music I listen to and organize the albums I rate and review in an aesthetically appealing manner.

**AlbumRater** is, as the name suggests, a web application that allows users to search, rate, and review albums, developed using **Spotify's Web API**. Once a new account is created, the user can search up any album in Spotify's database and, after selecting the specific album they are looking for from a list of most likely results, see an overview of its most important characteristics.

To save this album, the user must give it a rating of between 1 and 5 stars and, if desired, write a review for it. After the album has been saved, the user will be able to find it by going to their personal library, where they can sort their saved albums by:
* Newest
* Oldest
* Highest rated
* Lowest rated 

Another feature of the app is the Recents section where the user will be able to see the most recent reviews of the app's users and check their profiles which display some basic information about each user such as the number of ratings they have uploaded to the website, their average rating for albums, and a list of their ratings from newest to oldest. Any new rating created on the app will be automatically added to Recents.

## Technologies Used
For the front-end, I used **HTML**, **CSS**, and **JavaScript**. I also implemented the **Bootstrap** framework for additional styling and icons, and the website's font is Roboto, which I downloaded from **Google Fonts**.
For the back-end, I used **Python** and **SQL** (SQLite) via Django models.

## File-by-file Description 
(Including only files created / altered by me)

### Static
* `script.js`: This file includes almost of my JavaScript code (there is some more in `album.html` and `library.html`), including EventListeners for several buttons and forms within the program and all the functions below:

    * `get_token`: gets an API token to make fetch calls to the API

    * `search`: makes a fetch request to the API using the previously created token to search for albums matching the search parameters and displays the content of each album to the user

    * `view_album`: using an album's ID, it makes a fetch request to the API and saves detailed information about said album to the local storage (the displaying part is handled within the `album.html` view which this function redirects to)

    * `rate`: given the info from the number of stars the user wishes to give to the album, saves this information in the local storage as an integer and fills in the number of stars the user has clicked 

    * `save_album`: sends a fetch request to the backend with the album's information that then saves it to the database

    * `unsave_album`: sends a similar fetch request to the backend to unsave the rating from the database

    * `like_rating`: sends a fetch request to the backend with the rating's data to save it to the user's liked ratings and updates the page's styling to reflect that the rating has been liked

    * `unlike_rating`: sends a similar fetch request to the backend to unsave the rating from the user's liked rating and similarly updates the styling to reflect this change

* `styles.css`: Includes the enterity of my CSS styling, divided in sections for each view (except for login and register, which did not have a need for additional styling beyond Bootstrap's default) plus a general styling section. At the end of some sections there's also some extra styling to make the page look better in smaller screens if necessary.

### Templates
* `album.html`: Displays more detailed information about a specific album, including its title, artist, cover, release date, total number of tracks, and a list with the name of each track. This view also includes some JavaScript in it, which gets the album's data from the local memory and fills the page with it to display it to the user. 

    * If the user has not rated the album yet, they will be able to click on the stars to rate it and write a review (this part is optional). After clicking the Rate and Save button the save_album function will be triggered and the album will be saved to their library.

    * If the user has already rated the album, they will get to see their rating and review of it (if they chose to write one).

* `index.html`: The default landing page for the program, it initially provides the user with a simple search bar in which they can write the name of the album they are looking for. After clicking enter or the search button, the page dynamically displays the search results in this same page as cards with key information about each of them (title, artist, cover, and release date). Clicking on any of the albums will take the user to the album view that displays further information about it.

* `layout.html`: Includes the navigation menu and the template code that all the other templates inherit from. It also has the lines of code needed to get the custom font from Google Fonts and include Bootstrap and its icons.

* `library.html`: Displays cards with key information (title, artist, cover, and release date) for each album. Like the index view, clicking on any of the albums takes the user to the album view for it. This page also includes an option to sort the albums from newest, oldest, highest, or lowest rated, as well as some JavaScript used to hide and display the views for each sorting option as needed.

* `login.html`: Asks for the user's username and password to let them log into their account.

* `profile.html`: Displays information about a given user including their username, number of ratings, average rating, and a list of all their ratings.

* `recent.html`: Displays all the ratings made in the app from newest to oldest. It includes information about which user saved the album, what album they saved, the rating they gave it, and their review of it if they wrote one. This view uses Django's Paginator object to display ten ratings at a time; any more than this and anchor tags will appear at the bottom to move between pages.

* `register.html`:  Allows users to create an account by choosing a username and a password (which they are asked to repeat for confirmation). Users without an account will be able to search albums and see the information about them, but they won't get any of the other views nor the ability to rate or review albums.

### Others
* `admin.py`: Here is where my models User, Album, and Rating are registered.

* `models.py`: Where I create my models:

    * `User`: this model inherits from AbstractUser, but also includes the fields **groups**, **user_permissions**, **saved_albums** (ManyToManyField of Album objects), **liked_ratings** (ManyToManyField of Rating objects), and **ratings** (ManyToManyField of Rating objects for the ratings this User created)

    * `Album`: includes the fields **id** (the primary key), **name**, **img** (saves the url of the album's cover as a CharField), **artist**, and **release** (release date)

    * `Rating`: includes the fields **user** (ForeignKey for the User who created the rating), **album** (ForeignKey for the album the rating is for), **datetime** (stores the date and time the post was created for displaying and sorting purposes), **rating**, **review**, and **likes**.

*  `urls.py` (within rater directory): Includes all the url paths needed for my application to work. There is one for each of my Python functions and only two of them include any extra parameters: `album/<str:album_id>` and `profile/<str:username>/`.

* `views.py`: Here is the entirety of my python functions used to close the gap between my application's database and the frontend. These functions are:

    * `index`: displays the index page

    * `album`: given an albumID paremeter, checks whether the album is already in the current user's library and loads the album view with the correct information

    * `save_album`: gets an album's information from the frontend in the form of a JSON file. Then, creates a new instance of the Album object if there isn't one already and saves the album's data into it; then proceeds to create a new instance of the Rating object with the rating's information and saves it to the database. Returns a response to the frontend

    * `unsave_album`: gets an album's information from the frontend, then filters the ratings to find the one the user wants to delete and deletes it from the database. Returns a response to the frontend

    * `library`: sorts the current user's ratings in four different ways and displays the library view to the user

    * `recent`: creates a Paginator object with the ten most recent ratings and their data, then displays the recent view

    * `like_rating`: gets the rating's ID from the frontend and uses it to add the rating to the current user's liked_ratings field and to update the rating's like count

    * `unlike_rating`: much like like_rating, uses the rating's ID sent from the frontend to delete the rating from the current user's liked_ratings and update its like count

    * `profile`: given a username parameter, gets relevant information from the user by filtering the database and displays the profile view with said data

    * `login_view`: authenticates the user's information and checks if the username and password are valid, redirecting them to the index page if match

    * `logout_view`: logs the user out and redirects them to the index page

    * `register`: ensures that the username hasn't been already taken and that the initial password and the confirmation match. If everything goes well, redirects the user to the index page

* `settings.py`: I just added a single line to change the user model to use for authentification from the default one to my custom User model. 

* `urls.py` (within raterproject directory): I only added one line to include a path to my rater application. 

* `.gitignore`: Contains a list of files that I wish for git to ignore, including the database file created by SQLite, cache files, and `config.js`, which stores my private Spotify API key.

* `README.md`: The file you're reading right now! Detailing my project's functionality and explaining each file in it. **Thanks for reading!**

