import React,{useEffect, useMemo,useState} from 'react';
import {
	Table,
	Thead,
	Tbody,
	Tr,
	Th,
	Td,
	TableContainer,
	Modal,
	ModalOverlay,
	ModalContent,
	ModalHeader,
	ModalFooter,
	ModalBody,
	ModalCloseButton,
	useDisclosure,
	Button,
	HStack,
	Box,
	Checkbox,
	Input,
	VStack,
} from '@chakra-ui/react';
import AssetTable from './AssetTable';



function AssetSelect({setAssetSelected,assetsin}) {
	const { isOpen, onClose,onOpen, } = useDisclosure();
	const [selected,setSelected] = useState([]); 
	const save=()=>{
		console.log('Selected',selected);
		setAssetSelected(selected);
		onClose();
	};

	useEffect(() => {
		let preSelected=[];
		for (let i = 0; i < assetsin.length; i++) {
			let obj=assetsin[i];
			if (obj.hasOwnProperty('isSelected')&&obj.isSelected){
				preSelected.push(i);
			}
		}
		setSelected(preSelected);
	}, [assetsin]);
	

	return (<>
		<Button onClick={onOpen}>Select Assets</Button>
		<Modal isOpen={isOpen} onClose={onClose} size={'full'}>
			<ModalOverlay />
			<ModalContent>
				<ModalHeader>Asset Select</ModalHeader>
				<ModalCloseButton />
				<ModalBody >
					{assetsin && <AssetTable assets={assetsin} setSelectedAssets={setSelected} preSelIDs={selected}/>}
				</ModalBody>
				<ModalFooter>
					<HStack>
						<Button onClick={save}>Save</Button>
					</HStack>	
				</ModalFooter>
			</ModalContent>
			
		</Modal>
	</>
	);
}

export default AssetSelect;