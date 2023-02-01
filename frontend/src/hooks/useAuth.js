import { useContext, useEffect } from 'react';
import { createContext,useMemo,useState } from 'react';
import { loginUser } from '../api';
export const AuthContext = createContext({
	loggedIn:false,
	user: null,
	authError:null,
	login: () => null
});

export const AuthProvider = ({children}) => {
	const [user, setUser] = useState(null);
	const [loggedIn,setLoggedIn]=useState(false);
	const [authError, setAuthError] = useState(null);

	const login = ( username, password ) => {
		console.log({ username, password });
		loginUser({ username, password }).then(res=> {
			setUser(res.data);
			setLoggedIn(true);
			setAuthError(null);
		}).catch(err=>{
			setAuthError(err.response.data);
		});
	};
	const value = useMemo(
		() => ({loggedIn,user,authError,login}), 
		[user,authError]
	);

	return ( <AuthContext.Provider value={value}>
		{children}
	</AuthContext.Provider> );
};
const useAuth = () => {
	return (useContext(AuthContext));
};
 
export default useAuth;