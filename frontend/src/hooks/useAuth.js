import { useContext } from 'react';
import { createContext,useMemo,useState } from 'react';
export const AuthContext = createContext({
	setUser: () => null,
	user: null
});

export const AuthProvider = ({children}) => {
	const [user, setUser] = useState({'userID':1,'userType':'ADMIN','userPrivileges':'PUBLIC'});
	const value = useMemo(
		() => ({ user, setUser, }), 
		[user]
	);
	return ( <AuthContext.Provider value={value}>
		{children}
	</AuthContext.Provider> );
};
const useAuth = () => {
	return (useContext(AuthContext));
};
 
export default useAuth;