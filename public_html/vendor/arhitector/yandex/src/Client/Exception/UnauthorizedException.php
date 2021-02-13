<?php

/**
 * Часть библиотеки для работы с сервисами Яндекса
 *
 * @package    Arhitector\Yandex\Client\Exception
 * @version    2.0
 * @author     Arhitector
 * @license    MIT License
 * @copyright  2016 Arhitector
 * @link       https://github.com/jack-theripper
 */
namespace Arhitector\Yandex\Client\Exception;

use Http\Client\Exception;

/**
 * Исключение не авторизован.
 */
class UnauthorizedException extends \RuntimeException implements Exception
{
	/**
	 * Конструктор.
	 *
	 * @access  public
	 *
	 * @param   int        $code     Код исключения
	 * @param   string     $message  Сообщение исключения
	 * @param   \Exception $previous Предыдущее исключение
	 */
	public function __construct($message, $code = 401, \Exception $previous = null)
	{
		parent::__construct($message, $code, $previous);
	}
}