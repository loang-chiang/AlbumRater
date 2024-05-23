document.addEventListener('DOMContentLoaded', function() {

    // for when the user searches an album
    let formElement = document.querySelector('#search-form');
    if (formElement != null) {
        get_token(); // only gets token if in the index or library pages

        formElement.addEventListener('submit', function(event) {
            let searchInput = document.querySelector('#album-name').value;
            event.preventDefault();
            search(searchInput);
        });
    }

    // if the album is unsaved, lets user change the star rating
    let fluid = document.querySelectorAll('#stars-fluid'); 
    if (fluid.length > 0) {
        document.querySelectorAll('.bi-star, .bi-star-fill').forEach(star => {
            star.addEventListener('click', () => {
                let valueStr = star.dataset.value;
                let value = parseInt(valueStr);
                rate(value);
            })
        })
    }
    
    // creates new token if in library view
    let sortElement = document.querySelector('#sort-library');
    if (sortElement != null) {
        get_token(); // only gets token if in the index or library pages
    }

    // allows albums in library to be clickable and viewable 
    document.body.addEventListener('click', function(event) {
        let element = event.target;
        while (element && !element.classList.contains('album-div')) {
            element = element.parentElement;
        }
        if (element && element.classList.contains('album-div')) {
            let albumID = element.dataset.albumid;
            view_album(albumID);
        }
    });

    // saves and unsaves album
    document.body.addEventListener('click', function(event) {
        // gets album from local memory
        let album = JSON.parse(localStorage.getItem('album'));

        if (event.target.classList.contains('save-btn')) {
            let rating = 0;
            rating = parseInt((localStorage.getItem('rating')));
            let review = document.querySelector("#review").value;

            save_album(album, rating, review); // saves album to database
        }
        else if (event.target.classList.contains('unsave-btn')) {
            unsave_album(album);  // unsaves album
        }
    });

    // like and unlike rating
    document.body.addEventListener('click', function(event) {
        let ratingID = event.target.dataset.ratingId;
        if (event.target.classList.contains('bi-heart')) {
            like_rating(ratingID);
        }
        else if (event.target.classList.contains('bi-heart-fill')) {
            unlike_rating(ratingID);
        }
    });
});


// creates variable for access token and gets keys
import { clientId, clientSecret } from './config.js';
let access_token;


// gets api token
function get_token() {
    console.log("Calling get_token function");

    // create search parameters
    let params = new URLSearchParams();
    params.append('grant_type', 'client_credentials');
    params.append('client_id', clientId);
    params.append('client_secret', clientSecret);

    let authParams = {
        method: 'POST',
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: params.toString()
    };

    // fetch the token
    fetch("https://accounts.spotify.com/api/token", authParams)
    .then(result => result.json())
    .then(data => {
        console.log("Created a token!");
        access_token = data.access_token;
    });
}


// search function for albums
async function search(searchInput) {
    console.log("Calling search function");

    // creates variable for albums
    let albums = [];

    // gets the search parameters
    let albumParams = {
        method: 'GET',
        headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + access_token,
        },
    };

    // fetches the albums
    await fetch (
        "https://api.spotify.com/v1/search?q=" + searchInput + "&type=album", albumParams
    )
    .then(result => result.json())
    .then(data => {
        albums = data.albums.items; // gets an array of albums and sets the album array to them
        return albums; 
    })

    // prints info to the console
    console.log("Search Input: " + searchInput);
    for (let album of albums) {
        console.log("Album: " + album);
    }

    // empties albums' container
    document.querySelector(".albums-cont").innerHTML = "";

    // creates divs to display the albums
    albums.forEach(album => {
        // creates elements
        let album_cont = document.createElement('div'); 
        album_cont.classList.add('album-div');

        // allows them to be clickable
        album_cont.addEventListener('click', function() {
            let albumID = album.id;
            view_album(albumID);
        });

        let image = document.createElement('img');
        image.src = album.images[0].url;
        image.classList.add('album-img');

        let name = document.createElement('h3');
        name.textContent = album.name;
        name.classList.add('album-name');

        let artist_release = document.createElement('div');
        artist_release.classList.add('album-artist-release');

        let artist = document.createElement('h5');
        artist.innerHTML = "<strong>Artist: </strong>" + album.artists[0].name;
        artist.classList.add('album-artist');

        let release_date = document.createElement('h5');
        release_date.innerHTML = "<strong>Release date: </strong>" + album.release_date;
        release_date.classList.add('album-release');

        artist_release.appendChild(artist);
        artist_release.appendChild(release_date);

        // adds them to container
        album_cont.appendChild(image);
        album_cont.appendChild(name);
        album_cont.appendChild(artist_release);

        // adds them to albums' container
        document.querySelector(".albums-cont").appendChild(album_cont);
    })
}


// saves data
async function view_album(albumID) {
    console.log("Calling view_album function");

    // gets the search parameters
    let albumParams = {
        method: 'GET',
        headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + access_token,
        },
    };

    // fetch album data from id
    let album = await fetch (
        "https://api.spotify.com/v1/albums/" + albumID, albumParams
    )
    .then(result => result.json())
    .then(data => {
        return data;
    })

    // create variables to send data
    let tracks = [];
    for (let track of album.tracks.items) {
        tracks.push(track.name);
    }

    // saves variables in local storage
    localStorage.setItem('album', JSON.stringify(album));

    // runs album python function
    fetch(`/album/${album.id}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
    })
    .then(result => {
        // navigates to new page
        window.location.href = `/album/${album.id}`;
    })

    // there's some extra js inside the album.html file that fills it with the album's data :)
}


// changes the value of the album's rating
function rate(value) {
    console.log(`Calling the rate function for ${value} stars!`);

    document.querySelectorAll('.bi-star, .bi-star-fill').forEach(star => {
        if (star.dataset.value <= value && star.classList[1] == 'bi-star') {
            star.classList.replace('bi-star', 'bi-star-fill');
        }
        else if (star.dataset.value > value && star.classList[1] == 'bi-star-fill') {
            star.classList.replace('bi-star-fill', 'bi-star');
        }
    })
    localStorage.setItem('rating', value);  // saves user rating to local storage
}  


// sends fetch request to backend to save album in database
function save_album(album, rating, review) {
    console.log(`Calling save_album with ${album.name} and ${rating} stars`);

    if (rating == 0) {
        // shows user message
        alert('You need to rate the album to save it!')
    }
    else {
        // sends data to python func
        fetch('/save_album', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                albumID: album.id,
                albumName: album.name,
                albumImg: album.images[0].url,
                albumArtist: album.artists[0].name,
                albumRelease: album.release_date,
                rating: rating,
                review: review
            })
        })
        .then(response => response.json())
        .then(response => {
            console.log(response["message"]);

            // reloads page to reflect changes
            window.location.href = `/album/${album.id}`;
        })
    }
}


// unsaves album from user's database
function unsave_album(album) {
    console.log(`Calling save_album with ${album.name}`);

    // sends data to python func
    fetch('/unsave_album', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            album: album.id,
        })
    })
    .then(response => response.json())
    .then(response => {
        console.log(response["message"]);

        // reloads page to reflect changes
        window.location.href = `/album/${album.id}`;
    })
}


// likes a rating
function like_rating(ratingID) {
    console.log("Calling like_rating function");

    // sends data to python func
    fetch('/like_rating', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            ratingID: ratingID,
        })
    })
    .then(response => response.json())
    .then(response => {
        console.log(response["message"]);

        // updates innerHTML to reflect new like
        document.querySelector(`#like-count-${ratingID}`).innerHTML = response["likes"];
        document.querySelector(`#like-btn-${ratingID}`).classList.replace('bi-heart', 'bi-heart-fill');
    })
}

// unlikes a rating
function unlike_rating(ratingID) {
    console.log("Calling unlike_rating function");

    // sends data to python func
    fetch('/unlike_rating', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            ratingID: ratingID,
        })
    })
    .then(response => response.json())
    .then(response => {
        console.log(response["message"]);

        // update innerHTML to reflect one less like
        document.querySelector(`#like-count-${ratingID}`).innerHTML = response["likes"];
        document.querySelector(`#like-btn-${ratingID}`).classList.replace('bi-heart-fill', 'bi-heart');
    })
}