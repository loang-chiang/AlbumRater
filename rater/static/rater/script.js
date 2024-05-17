document.addEventListener('DOMContentLoaded', function() {

    // for when the user searches an album
    let formElement = document.querySelector('#search-form');
    if (formElement != null) {
        get_token(); // only get token if in the index page

        formElement.addEventListener('submit', function(event) {
            let searchInput = document.querySelector('#album-name').value;
            event.preventDefault();
            search(searchInput);
        });
    }
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

        let name = document.createElement('h2');
        name.textContent = album.name;
        name.classList.add('album-name');

        let release_date = document.createElement('h4');
        release_date.innerHTML = 'Release date:' + album.release_date;
        release_date.classList.add('album-release');

        // adds them to container
        album_cont.appendChild(image);
        album_cont.appendChild(name);
        album_cont.appendChild(release_date);

        // adds them to the body
        document.body.appendChild(album_cont);
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

    // navigates to new page
    window.location.href = '/album';

    // there's some extra js inside the album.html file that fills it with the album's data :)
}