document.addEventListener('DOMContentLoaded', function() {
    get_token();
    document.querySelector('#search-form').addEventListener('submit', function(event) {
        let searchInput = document.querySelector('#album-name').value;
        event.preventDefault();
        search(searchInput);
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

    // fetches the album's ID
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
        console.log("Album: " + album.id);
    }

    // creates divs to display the albums
    albums.forEach(album => {
        // creates elements
        let album_cont = document.createElement('div'); 
        let image = document.createElement('img');
        image.src = album.images[0].url;
        let name = document.createElement('h4');
        name.innerHTML = album.name;
        let release_date = document.createElement('h4');
        release_date.innerHTML = 'Release date:' + album.release_date;

        // adds them to container
        album_cont.appendChild(image);
        album_cont.appendChild(name);
        album_cont.appendChild(release_date);

        // adds them to the body
        document.body.appendChild(album_cont);
    })
}