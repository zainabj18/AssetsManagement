import { useContext,useEffect } from 'react';
import { createContext,useMemo,useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginUser,indentifyUser,logoutUser} from '../api';
export const AuthContext = createContext({
	loggedIn:true,
	user: null,
	authError:null,
	login: () => null,
	loaded: true,
	logout: () => null,
});
// holds global state on if user is logged in
export const AuthProvider = ({children}) => {
	let navigate = useNavigate();
	const [user, setUser] = useState(null);
	const [loggedIn,setLoggedIn]=useState(false);
	const [authError, setAuthError] = useState(null);
	const [loaded,setLoaded]=useState(false);

	const logout=()=> {
		logoutUser().catch(() => {}).finally(()=>{
			setUser(null);
			setLoggedIn(false);
			navigate('/login');
		});
		
	};
	const login = ( username, password ) => {
		loginUser({ username, password }).then(res=> {
			setUser(res.data);
			setLoggedIn(true);
			setAuthError(null);
			navigate('/assets/');
		}).catch(err=>{
			setAuthError(err.response.data);
			
		});
	};

	useEffect(() => {
		const fetchData = async () => {
			const res = await indentifyUser().then(res => {
				setUser(res.data);
				setLoggedIn(true);
			}).catch((res) => {
				console.log(res);
			}).finally(()=>{
				setLoaded(true);
			});
			return res;
		  };
		fetchData();
		console.log('Auth mounted');
	},[]);
	const value = useMemo(
		() => ({loggedIn:true,user,authError,login,loaded,logout}), 
		[user,authError,loggedIn]
	);

	console.log("XXXX",value)
	return ( <AuthContext.Provider value={value}>
		{loaded&&children}
	</AuthContext.Provider> );
};
const useAuth = () => {
	return (useContext(AuthContext));
};
 
export default useAuth;