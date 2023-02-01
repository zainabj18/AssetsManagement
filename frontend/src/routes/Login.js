import React, { useState } from 'react';
import {
	FormControl,
	FormLabel,
	Input,
	Button,
	InputGroup,
	InputRightElement,
	Container,
	VStack,
	IconButton
} from '@chakra-ui/react';
import { ViewIcon,ViewOffIcon } from '@chakra-ui/icons';

function Login() {
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');
	const [isAuthenticated, setIsAuthenticated] = useState(false);
	const [show, setShow] = React.useState(false);
	const [error, setError] = useState('');
	const handleLogin = () => {
		try {
			console.log('I am here');
			fetch('/api/v1/auth/login', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'Access-Control-Allow-Origin': 'true',
				},
				body: JSON.stringify({ username, password }),
			}).then((res) =>
				res.json().then((data) => {
					console.log('hello');
					console.log('Bye');
					console.log(data);
					if (data.isAuthenticated) {
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
			<VStack>
				<FormControl>
					<FormLabel htmlFor="username">Username</FormLabel>
					<Input
						type="text"
						id="username"
						value={username}
						onChange={(e) => setUsername(e.target.value)}
					/>
				</FormControl>
				<FormControl>
					<FormLabel htmlor="password">Password</FormLabel>
					<InputGroup>
						<Input
							type={show ? 'text' : 'password'}
							id="password"
							placeholder="Enter password"
							value={password}
							onChange={(e) => setPassword(e.target.value)}
						/>
						<InputRightElement>
							<IconButton size='xs'
								onClick={()=>setShow(!show)} icon={show ? <ViewIcon /> : <ViewOffIcon />} />
						</InputRightElement>
					</InputGroup>
				</FormControl>
				<Button onClick={handleLogin}>
          Login
				</Button>
			</VStack>
		</Container>
	);
}

export default Login;
