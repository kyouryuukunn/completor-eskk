if exists('g:loaded_completor_eskk_plugin')
  finish
endif

let g:loaded_completor_eskk_plugin = 1
let s:py = has('python3') ? 'py3' : 'py'


function! s:err(msg)
  echohl Error
  echo a:msg
  echohl NONE
endfunction


function! s:import_eskk()
  try
    exe s:py 'import completor_eskk'
  catch /^Vim(py\(thon\|3\)):/
    call s:err('Fail to import completor_eskk')
    return
  endtry

  try
    exe s:py 'import completor, completers.common'
  catch /^Vim(py\(thon\|3\)):/
    call s:err('Fail to import completor')
    return
  endtry

  try
    exe s:py 'completor.get("common").hooks.append(completor_eskk.Eskk.filetype)'
  catch /^Vim(py\(thon\|3\)):/
    call s:err('Fail to add eskk hook')
  endtry
endfunction


function! s:enable()
  call s:import_eskk()
  call s:disable()
endfunction


function! s:disable()
  augroup completor_eskk
    autocmd!
  augroup END
endfunction


augroup completor_eskk
  autocmd!
  autocmd InsertEnter * call s:enable()
augroup END
