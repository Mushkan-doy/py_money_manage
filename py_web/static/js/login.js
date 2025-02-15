$(document).ready(function() {
    $(document).on('submit', '#loginForm', function(event) {
        event.preventDefault();
        var email = $('#loginForm input[name="email"]').val();
        var password = $('#loginForm input[name="password"]').val();
        console.log("email : ", email);
        console.log("password : ", password);
        console.log("API_DOMAIN : ", API_DOMAIN);
        $.ajax({
            url: `${API_DOMAIN}login`,
            type: 'POST',
            data: {
                "email": email,
                "password": password
            },
            success: function(response) {
                console.log("response : ", response.data);
                if (response.status_code == 200 ) {
                    window.localStorage.setItem('token', {access_token: response.data.access, refresh_token: response.data.refresh});
                    window.localStorage.setItem('email', response.data.email);
                    window.localStorage.setItem('first_name', response.data.first_name);
                    window.localStorage.setItem('last_name', response.data.last_name);
                    window.location.href = '/dashboard';
                } else {
                    document.querySelector('.card-category').innerHTML = '<span class="text-danger">'+ data.MESSAGE +'</span>';
                }
            },
            error : function(error){
                console.log("error : ", error);
            }
        });
    })
});