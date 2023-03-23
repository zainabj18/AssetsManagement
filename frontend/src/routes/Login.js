import React, { useState } from 'react';
import {
	Avatar,
	Text,
	Flex, useMediaQuery,
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
	Card
} from '@chakra-ui/react';
import { ViewIcon, ViewOffIcon } from '@chakra-ui/icons';
import useAuth from '../hooks/useAuth';
/**
 * Component for login for user.
 *
 * @component
 * @example
 * const username = admin
 * const password = 'admin'
 
 */
function Login() {
	const [isSmallerThan745] = useMediaQuery('(max-width: 744px)');
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');
	const [show, setShow] = React.useState(false);
	const { login, authError } = useAuth();
	const handleLogin = () => {
		login(username, password);
	};

	return (

		<Flex
			flexDirection='column'
			width='100wh'
			height='100vh'
			justifyContent='center'
			alignItems='center'
			alignSelf={'center'}
			bgGradient='linear(to-l, #4E65FF, #92EFFD)'
		>
			<VStack flexDir='column'
				mb='2'
				justifyContent='center'
				alignItems='center'
				width={'100%'}

			>
				<Card paddingX={10} paddingY={10} width={isSmallerThan745 ? '90%' : '45%'} boxShadow='xl' p='6' rounded='md' bg='white' borderRadius={10}>
					<Avatar bg='#4E65FF' alignSelf={'center'} />
					<Text fontSize='4xl' textAlign={'center'}>Login</Text>
					<FormControl marginTop={5}>
						<FormLabel>Username</FormLabel>
						<Input
							bg='#fff'
							border={'1px solid gray'}
							paddingY={6}
							type='text'
							placeholder='Enter username'
							value={username}
							onChange={(e) => setUsername(e.target.value)}
						/>
					</FormControl>
					<FormControl marginTop={10}>
						<FormLabel>Password</FormLabel>
						<InputGroup >
							<Input
								bg='#fff'
								border={'1px solid gray'}
								paddingY={6}
								type={show ? 'text' : 'password'}
								placeholder='Enter password'
								value={password}
								onChange={(e) => setPassword(e.target.value)}
							/>
							<InputRightElement>
								<IconButton size='xs'
									onClick={() => setShow(!show)} icon={show ? <ViewIcon /> : <ViewOffIcon />} />
							</InputRightElement>
						</InputGroup>
					</FormControl>
					{authError && (<Alert status='error'>
						<AlertIcon />
						<AlertTitle>{authError.error}</AlertTitle>
						<AlertDescription>{authError.msg}</AlertDescription>
					</Alert>)}
					<Button onClick={handleLogin} marginTop={10} bg='#4E65FF' opacity={'0.8'} paddingY={6}>
						Login
					</Button>
				</Card>
			</VStack>
		</Flex>

	);
}

export default Login;
