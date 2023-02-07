import React, { useState } from 'react';
import { FormControl, FormLabel, Input, Button, useColorMode, Container, Center, Box, Heading } from '@chakra-ui/react';

function Login() {

	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');
	const [isAuthenticated, setIsAuthenticated] = useState(false);
	const [error, setError] = useState('');
	const {colorMode, toggleColorMode } = useColorMode();
	const [show, setShow] = React.useState(false);
	const handleClick = () => setShow(!show);

    
	const handleLogin = () => {
		try {
			console.log('I am here');
			fetch('https://localhost:5000/api/v1/auth/login',{
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'Access-Control-Allow-Origin': 'true'
				},
				body: JSON.stringify({username,
					password})}).then((res) =>
				res.json().then((data) => {
					console.log('hello');
					console.log('Bye');
					if (data.isAuthenticated){
						setIsAuthenticated(true);
						setError('');
					}
				})
			);
			
		} catch (error) {
			console.error(error);
			setError('Invalid username or password');
		}
	};

	return (
		<Container>
			<Center height={'100vh'}>
				<Box bg={'white'} color={'black'} p={10} borderRadius={10} mb={'50px'}>
					<div style={{ position: 'absolute', top: '0', right: '0'}}>
						<button style={{ border: '1px solid #ccc'}} onClick={toggleColorMode}> {colorMode === 'light' ?  'Dark' : 'Light'} </button>
					</div>
					{isAuthenticated ? (
						<div>Welcome!</div>
					) : (
						<form>
							<Heading mb={3}>Login Form</Heading>
							<FormControl>
								<FormLabel htmlFor='username'>Username</FormLabel>
								<Input type='text' id='username' value={username} onChange={e => setUsername(e.target.value)}/>
							</FormControl>
							<FormControl>
								<FormLabel htmlFor='password'>
									<div style={{ position: 'absolute', top: '0'}}>
                    Password
									</div>
								</FormLabel>
								<Input type={show ? 'text' : 'password'} id='password' pr='4.5rem' top='7' placeholder='Enter password' value={password} onChange={e => setPassword(e.target.value)}/>
								<Button w={65} h='1.95rem' top='-2' left='calc(100% - 70px)' size='sm' onClick={handleClick}>
									{show ? 'Hide' : 'Show'}
								</Button>
							</FormControl>

							<Button variantColor="teal" mt={'4'} onClick={handleLogin}>
                Login
							</Button>
						</form>
					)}
					{error && <div style={{color: 'red'}}>{error}</div>}
				</Box>
			</Center>
		</Container>
	);
}

export default Login;
