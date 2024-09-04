export const login = async (username, password) => {
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        if (!response.ok) {
            throw new Error('Invalid credentials');
        }

        const data = await response.json();
        localStorage.setItem('token', data.token);
        return true;
    } catch (error) {
        console.error('Error during login:', error);
        return false;
    }
};

export const getToken = () => {
    return localStorage.getItem('token');
};

export const isLoggedIn = () => {
    return !!localStorage.getItem('token');
};

export const logout = () => {
    localStorage.removeItem('token');
};
