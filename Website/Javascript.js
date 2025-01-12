        function openTab(event, tabId) {
            // Remove active class
            const tabs = document.querySelectorAll('.tab');
            const contents = document.querySelectorAll('.content');

            tabs.forEach(tab => tab.classList.remove('active'));
            contents.forEach(content => content.classList.remove('active'));

            // Add active class 
            event.currentTarget.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        }

        function initMap() {
            const map = new google.maps.Map(document.getElementById("map"), {
                center: { lat: -34.397, lng: 150.644 },
                zoom: 8,
            });
        }
