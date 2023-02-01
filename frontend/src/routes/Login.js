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
	IconButton,
	Alert,
	AlertIcon,
	AlertTitle,
	AlertDescription,
} from '@chakra-ui/react';
import axios from 'axios';
import { ViewIcon,ViewOffIcon } from '@chakra-ui/icons';

function Login() {
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');
	const [isAuthenticated, setIsAuthenticated] = useState(false);
	const [show, setShow] = React.useState(false);
	const [error, setError] = useState(null);
	const handleLogin = () => {
		axios.post('/api/v1/auth/login',{username, password}).then((res) => {
			console.log(res);
			setError(null);
		}
		).catch( (res) =>{
			setError(res.response.data);
		});};

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
				{error && (<Alert status='error'>
  							<AlertIcon />
					<AlertTitle>{error.error}</AlertTitle>
					<AlertDescription>{error.msg}</AlertDescription>
				</Alert>)}
				<Button onClick={handleLogin}>
          Login
				</Button>
			</VStack>
		</Container>
	);
}

export default Login;
