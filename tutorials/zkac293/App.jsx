import React from "react";
import { Button, ButtonGroup } from '@chakra-ui/react'

function App() {
    return(
        <ChakraProvider>
            <Stack spacing={6} direction='row' align='center'>
                <Box
                    m="8px"
                    p="8px"
                    border="1px"
                    rounded="10px"
                    borderColor="gray.300"
                    boxShadow="md"
                    bg="lavender"
                    color="#2d383c"
                    fontSize="2rem"
                    textAlign="center"
                    fontFamily="Consolas"
                    w="400px"
                    h="400px"
                >
                    Hello, World!{" "}
                </Box>
                <Button colorScheme='purple' size='xs'>
                    Hello, World!
                </Button>
                <Button colorScheme='pink' size='sm'>
                    Button
                </Button>
                <Button colorScheme='linkedin' size='md'>
                    Settings
                </Button>
                <Button colorScheme='yellow' size='lg'>
                    Blue Lock
                </Button>
            </Stack>
        </ChakraProvider>
    );
}

export default App;