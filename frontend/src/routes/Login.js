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
import useAuth from '../hooks/useAuth';

function Login() {
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');
	const [show, setShow] = React.useState(false);
	const { login,authError } = useAuth();
	const handleLogin = () => {
		login(username,password);};

	return (
		<Container>
			<VStack>
				<FormControl>
					<FormLabel>Username</FormLabel>
					<Input
						type="text"
						placeholder="Enter username"
						value={username}
						onChange={(e) => setUsername(e.target.value)}
					/>
				</FormControl>
				<FormControl>
					<FormLabel>Password</FormLabel>
					<InputGroup>
						<Input
							type={show ? 'text' : 'password'}
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
				{authError && (<Alert status='error'>
  							<AlertIcon />
					<AlertTitle>{authError.error}</AlertTitle>
					<AlertDescription>{authError.msg}</AlertDescription>
				</Alert>)}
				<Button onClick={handleLogin}>
          Login
				</Button>
			</VStack>
		</Container>
	);
}

export default Login;
