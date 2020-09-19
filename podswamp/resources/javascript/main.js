/* A little javascript to enhance the abilities of the playback pages a little */

class PlaybackControl{
    constructor(playbackElementId, playbackModalId){
        this.playbackElement = document.getElementById(playbackElementId);
        this.playbackModal = $(`#${playbackModalId}`);
        this.dialog = this.playbackModal.dialog({
            autoOpen: false,
            width: "80%",
            modal: true,
            buttons: {
                Yes: function(){
                    this.playbackElement.play();
                    this.playbackElement.dialog("close");
                }.bind(this),
                No: function(){
                    this.playbackElement.currentTime = 0;
                    this.playbackElement.dialog("close");
                }.bind(this)
            }
        });

        let data = this.readFromUrl();
        if(data.vts){
            let vts = parseInt(data.vts, 10);
            if(vts){
                this.playbackElement.currentTime = vts;
            }
        }
        if(data.vte){
            let vte = parseInt(data.vte, 10);
            let interval = setInterval(function(){
                if(this.playbackElement.currentTime >= vte){
                    this.playbackElement.pause();
                    clearInterval(interval);
                }
            }.bind(this), 1000);

            if(data.title){
                this.dialog.dialog("options", "title", "Playing a clip!");
                this.dialog.dialog("open");
            }else{
                this.dialog.dialog("open");
            }
        }
    }

    readFromUrl(){
        //Adapted from https://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript
        let query = window.location.search;
        return query
            ? (/^[?#]/.test(query) ? query.slice(1) : query)
                .split('&')
                .reduce((params, param) => {
                        let [key, value] = param.split('=');
                        params[key] = value ? decodeURIComponent(value.replace(/\+/g, ' ')) : '';
                        return params;
                    }, {}
                )
            : {};
    }
}

const playbackControl = new PlaybackControl("playback", "playback-modal");
