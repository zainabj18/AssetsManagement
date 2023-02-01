import { useContext,useEffect } from 'react';
import { createContext,useMemo,useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginUser,indentifyUser } from '../api';
export const AuthContext = createContext({
	loggedIn:false,
	user: null,
	authError:null,
	login: () => null,
	loaded: false
});

export const AuthProvider = ({children}) => {
	let navigate = useNavigate();
	const [user, setUser] = useState(null);
	const [loggedIn,setLoggedIn]=useState(false);
	const [authError, setAuthError] = useState(null);
	const [loaded,setLoaded]=useState(false);
	const login = ( username, password ) => {
		loginUser({ username, password }).then(res=> {
			setUser(res.data);
			setLoggedIn(true);
			setAuthError(null);
			navigate('/');
		}).catch(err=>{
			setAuthError(err.response.data);
		});
	};

	useEffect(() => {
		console.log('is loaded');
		console.log(loaded);
		indentifyUser().then(res => {
			console.log('Auth mounted');
			console.log(res.data);
			setUser(res.data);
			setLoggedIn(true);
		}).catch(() => {}).finally(setLoaded(true));
	},[]);
	const value = useMemo(
		() => ({loggedIn,user,authError,login,loaded}), 
		[user,authError]
	);

	return ( <AuthContext.Provider value={value}>
		{loaded && children}
	</AuthContext.Provider> );
};
const useAuth = () => {
	return (useContext(AuthContext));
};
 
export default useAuth;