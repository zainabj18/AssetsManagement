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
/**
 * 
 * hook for checkinh auth state using context api
 * @param {*} childern 
 * @returns 
 */
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

	/**

loginUser - A function that makes an API call to log in the user with the provided credentials.
@param {Object} credentials - An object containing the user's credentials.
@param {string} credentials.username - The username of the user.
@param {string} credentials.password - The password of the user.
@returns {Promise} - A Promise that resolves with the user data if the login is successful, and rejects with an error if the login fails.
*/
/**

setUser - A function that sets the current user in the application state.
@param {Object} user - An object containing the user's data.
*/
/**

setLoggedIn - A function that sets the user's logged-in status in the application state.
@param {boolean} isLoggedIn - A boolean representing the user's logged-in status.
*/
/**

setAuthError - A function that sets any authentication errors in the application state.
@param {Object|null} error - An object containing the authentication error data, or null if there are no errors.
*/
/**

navigate - A function that navigates to the specified page.
@param {string} page - The URL of the page to navigate to.
*/

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
/** 
	A component that provides authentication context to its children.
@param {Object} props - The component props.
@param {boolean} props.loaded - A boolean representing whether the authentication data has been loaded.
@param {ReactNode} props.children - The child components that will have access to the authentication context.
@returns {JSX.Element} - The JSX element that wraps the child components with the authentication contex
**/
	return ( <AuthContext.Provider value={value}>
		{loaded&&children}
	</AuthContext.Provider> );
};
const useAuth = () => {
	return (useContext(AuthContext));
};
 
export default useAuth;